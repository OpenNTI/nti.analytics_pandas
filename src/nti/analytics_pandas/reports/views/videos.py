#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: videos.py 77243 2015-11-17 13:12:59Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import VideoEventsTimeseries
from ...analysis import VideoEventsTimeseriesPlot

from .commons import build_plot_images_dictionary
from .commons import get_course_names

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class VideosTimeseriesContext(object):

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

Context = VideosTimeseriesContext

class VideosTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Videos Related Events')

	def _build_data(self, data=_('sample Videos related events report')):
		if 'has_video_data' not in self.options.keys():
			self.options['has_video_data'] = False

		if 'has_video_watched_data' not in self.options.keys():
			self.options['has_video_watched_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		self.vet =  VideoEventsTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses)
		if self.vet.dataframe.empty:
			self.options['has_video_data'] = False
			return self.options
		
		self.options['has_video_data'] = True
		
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))

		data = {}
		data  = self.generate_video_events_plots(data)
		self._build_data(data)
		return self.options

	def generate_video_events_plots(self, data):
		self.vetp = VideoEventsTimeseriesPlot(self.vet)
		data = self.generate_video_watched_plots(data)
		return data

	def generate_video_watched_plots(self, data):
		plots = self.vetp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_seaborn_,
										 video_event_type = 'watch')
		if plots:
			data['videos_watched'] = build_plot_images_dictionary(plots)
			self.options['has_video_watched_data'] = True
		return data

View = VideosTimeseriesReport = VideosTimeseriesReportView
