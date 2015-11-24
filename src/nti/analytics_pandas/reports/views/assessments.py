#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: notes.py 77689 2015-11-24 10:06:00Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import AssignmentViewsTimeseries
from ...analysis import AssignmentsTakenTimeseries
from ...analysis import AssessmentEventsTimeseries
from ...analysis import SelfAssessmentViewsTimeseries
from ...analysis import SelfAssessmentsTakenTimeseries
from ...analysis import AssignmentViewsTimeseriesPlot
from ...analysis import AssignmentsTakenTimeseriesPlot
from ...analysis import AssessmentEventsTimeseriesPlot
from ...analysis import SelfAssessmentViewsTimeseriesPlot
from ...analysis import SelfAssessmentsTakenTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class AssessmentsEventsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True,
				 number_of_most_active_user=10):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_seaborn_ = theme_seaborn_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user

Context = AssessmentsEventsTimeseriesContext

class AssessmentsEventsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Assessments Related Events')

	def _build_data(self, data=_('sample assessments related events report')):
		keys = self.options.keys()

		if 'has_assignment_taken_data' not in keys:
			self.options['has_assignment_taken_data'] = False

		if 'has_assignment_views_data' not in keys:
			self.options['has_assignment_views_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		
		self.att = AssignmentsTakenTimeseries(self.context.session,
										      self.context.start_date,
										      self.context.end_date,
										      self.context.courses)
		
		if self.att.dataframe.empty:
			self.options['has_assignment_taken_data'] = False
		else:
			self.options['has_assignment_taken_data'] = True
			data = self.generate_assignments_taken_plots(data)


		self.avt = AssignmentViewsTimeseries(self.context.session,
										     self.context.start_date,
										     self.context.end_date,
										     self.context.courses)

		if self.avt.dataframe.empty:
			self.options['has_assignment_views_data'] = False
		else:
			self.options['has_assignment_views_data'] = True
			data = self.generate_assignment_view_plots(data)

		self._build_data(data)
		return self.options

	def generate_assignments_taken_plots(self, data):
		self.attp = AssignmentsTakenTimeseriesPlot(self.att)
		data = self.get_assignments_taken_plots(data)
		data = self.get_assignments_taken_plots_per_device_types(data)
		data = self.get_assignments_taken_plots_per_enrollment_types(data)
		if len(self.context.courses) > 1:
			data = self.get_assignments_taken_plots_per_course_sections(data)
		else:
			self.options['has_assignment_taken_per_course_sections'] = False
		return data

	def get_assignments_taken_plots(self, data):
		plots = self.attp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_seaborn_)
		if plots:
			data['assignment_taken'] = build_plot_images_dictionary(plots)
		return data

	def get_assignments_taken_plots_per_device_types(self, data):
		plots = self.attp.analyze_events_group_by_device_type(self.context.period_breaks,
															  self.context.minor_period_breaks,
															  self.context.theme_seaborn_)
		
		self.options['has_assignment_taken_per_device_types'] = False
		if plots:
			data['assignment_taken_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_taken_per_device_types'] = True
		return data

	def get_assignments_taken_plots_per_enrollment_types(self, data):
		plots = self.attp.analyze_events_group_by_enrollment_type(self.context.period_breaks,
																  self.context.minor_period_breaks,
																  self.context.theme_seaborn_)
		
		self.options['has_assignment_taken_per_enrollment_types'] = False
		if plots:
			data['assignment_taken_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_taken_per_enrollment_types'] = True
		return data

	def get_assignments_taken_plots_per_course_sections(self, data):
		plots = self.attp.analyze_events_per_course_sections(self.context.period_breaks,
															 self.context.minor_period_breaks,
															 self.context.theme_seaborn_)
		self.options['has_assignment_taken_per_course_sections'] = False
		if plots:
			data['assignment_taken_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_assignment_taken_per_course_sections'] = True
		return data

	def generate_assignment_view_plots(self, data):
		self.avtp = AssignmentViewsTimeseriesPlot(self.avt)
		data = self.get_assignment_view_plots(data)
		data = self.get_assignment_view_plots_per_device_types(data)
		return data

	def get_assignment_view_plots(self, data):
		plots = self.avtp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_seaborn_)
		if plots:
			data['assignment_views'] = build_plot_images_dictionary(plots)
		return data

	def get_assignment_view_plots_per_device_types(self, data):
		plots = self.avtp.analyze_events_group_by_device_type(self.context.period_breaks,
															  self.context.minor_period_breaks,
															  self.context.theme_seaborn_)
		self.options['has_assignment_views_per_device_types'] = False
		if plots:
			data['assignment_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_views_per_device_types'] = True
		return data
	
View = AssessmentsEventsTimeseriesReport = AssessmentsEventsTimeseriesReportView
