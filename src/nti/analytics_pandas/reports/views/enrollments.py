#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: enrollments.py 77820 2015-11-26 16:09:09Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import CourseCatalogViewsTimeseries
from ...analysis import CourseCatalogViewsTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class EnrollmentTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks='1 week', minor_period_breaks='1 day', 
				 theme_seaborn_=True, number_of_most_active_user=10):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_seaborn_ = theme_seaborn_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user

Context = EnrollmentTimeseriesContext

class EnrollmentTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Enrollment Related Events')

	def _build_data(self, data=_('sample enrollment related events report')):
		keys = self.options.keys()
		if 'has_catalog_view_data' not in keys:
			self.options['has_catalog_view_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		self.ccvt = CourseCatalogViewsTimeseries(self.context.session,
											   	  self.context.start_date,
											   	  self.context.end_date,
												  self.context.courses)
		if self.ccvt.dataframe.empty:
			self.options['has_catalog_view_data'] = False
		else:
			self.options['has_catalog_view_data'] = True
			data = self.generate_catalog_view_plots(data)

		self._build_data(data)
		return self.options

	def generate_catalog_view_plots(self, data):
		self.ccvtp = CourseCatalogViewsTimeseriesPlot(self.ccvt)
		data = self.get_catalog_view_plots(data)
		data = self.get_catalog_view_plots_per_device_types(data)
		return data

	def get_catalog_view_plots(self, data):
		plots = self.ccvtp.explore_events(self.context.period_breaks,
										  self.context.minor_period_breaks,
										  self.context.theme_seaborn_)
		if plots:
			data['course_catalog_views'] = build_plot_images_dictionary(plots)
		return data

	def get_catalog_view_plots_per_device_types(self, data):
		plots = self.ccvtp.analyze_device_types(self.context.period_breaks,
											    self.context.minor_period_breaks,
											    self.context.theme_seaborn_)
		self.options['has_course_catalog_views_per_device_types'] = False
		if plots:
			data['course_catalog_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_course_catalog_views_per_device_types'] = True
		return data

View = EnrollmentTimeseriesReport = EnrollmentTimeseriesReportView
