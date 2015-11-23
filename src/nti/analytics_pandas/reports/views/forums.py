#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: forums.py 77243 2015-11-17 13:12:59Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import ForumsCreatedTimeseries
from ...analysis import ForumCommentLikesTimeseries
from ...analysis import ForumCommentFavoritesTimeseries
from ...analysis import ForumsCommentsCreatedTimeseries

from ...analysis import ForumsEventsTimeseriesPlot
from ...analysis import ForumsCreatedTimeseriesPlot
from ...analysis import ForumCommentLikesTimeseriesPlot
from ...analysis import ForumsCommentsCreatedTimeseriesPlot
from ...analysis import ForumCommentFavoritesTimeseriesPlot

from .commons import build_plot_images_dictionary
from .commons import  build_images_dict_from_plot_dict
from .commons import get_course_names

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class ForumsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks=None, minor_period_breaks=None, theme_seaborn_=True,
				 number_of_most_active_user=10):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_seaborn_ = theme_seaborn_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user

Context = ForumsTimeseriesContext

class ForumsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Forums Related Events')

	def _build_data(self, data=_('sample forums related events report')):
		keys = self.options.keys()
		if 'has_forums_created_data' not in keys:
			self.options['has_forums_created_data'] = False

		if 'has_forums_created_data_per_device_types' not in keys:
			self.options['has_forums_created_data_per_device_types'] = False
			
		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))

		self.fct = ForumsCreatedTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses)
		if self.fct.dataframe.empty:
			self.options['has_forums_created_data'] = False
			return self.options
		self.options['has_forums_created_data'] = True

		data = {}
		data = self.generate_forums_created_plots(data)
		self._build_data(data)

		return self.options

	def generate_forums_created_plots(self, data):
		self.fctp  = ForumsCreatedTimeseriesPlot(self.fct)
		data = self.get_forums_created_plots(data)
		return data

	def get_forums_created_plots(self, data):
		plots = self.fctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_seaborn_)
		if plots:
			data['forums_created'] = build_plot_images_dictionary(plots)
		return data

	def get_forums_created_plots_per_device_types(self, data):
		plots = self.fctp.analyze_device_types(self.context.period_breaks,
										       self.context.minor_period_breaks,
										 	   self.context.theme_seaborn_)
		if plots:
			data['forums_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_forums_created_data_per_device_types'] = True
		return data

View = ForumsTimeseriesReport = ForumsTimeseriesReportView
