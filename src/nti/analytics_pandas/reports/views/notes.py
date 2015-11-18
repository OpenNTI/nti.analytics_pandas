#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import NotesCreationTimeseries
from ...analysis import NotesCreationTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class NoteEventsTimeseriesContext(object):

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

Context = NoteEventsTimeseriesContext

class NoteEventsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Notes Related Events')

	def _build_data(self, data=_('sample notes related events report')):
		if 'has_notes_created_data' not in self.options.keys():
			self.options['has_notes_created_data'] = False
		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ",".join(map(str, course_names))
		data = {}

		self.nct = NotesCreationTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses)
		if self.nct.dataframe.empty:
			self.options['has_notes_created_data'] = False
		else:
			self.options['has_notes_created_data'] = True

		if self.options['has_notes_created_data']:
			data = self.generate_notes_created_plots(data)

		self._build_data(data)
		print (self.options)
		return self.options

	def generate_notes_created_plots(self, data):
		self.nctp = NotesCreationTimeseriesPlot(self.nct)
		data = self.get_notes_created_plots(data)
		data = self.get_notes_created_per_device_types_plots(data)
		data = self.get_notes_created_per_resource_types_plots(data)
		data = self.get_notes_created_per_sharing_types_plots(data)
		data = self.get_notes_created_per_course_sections_plots(data)
		data = self.get_notes_created_the_most_active_users(data)
		return data

	def get_notes_created_plots(self, data):
		plots = self.nctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_seaborn_)
		if plots:
			data['notes_created'] = build_plot_images_dictionary(plots)
		return data

	def get_notes_created_per_device_types_plots(self, data):
		plots = self.nctp.analyze_device_types(self.context.period_breaks,
										 	   self.context.minor_period_breaks,
										 	   self.context.theme_seaborn_)
		self.options['has_notes_created_data_per_device_types'] = False
		if plots:
			print('HERE')
			print(plots)
			data['notes_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_notes_created_data_per_device_types'] = True
		return data

	def get_notes_created_per_resource_types_plots(self, data):
		plots = self.nctp.analyze_resource_types(self.context.period_breaks,
										 		 self.context.minor_period_breaks,
										 		 self.context.theme_seaborn_)
		if plots:
			data['notes_created_per_resource_types'] = build_plot_images_dictionary(plots)
		return data

	def get_notes_created_per_sharing_types_plots(self, data):
		plots = self.nctp.analyze_sharing_types(self.context.period_breaks,
										 		self.context.minor_period_breaks,
										 		self.context.theme_seaborn_)
		if plots:
			data['notes_created_per_sharing_types'] = build_plot_images_dictionary(plots)
		return data

	def get_notes_created_per_course_sections_plots(self, data):
		plots = self.nctp.analyze_events_per_course_sections(self.context.period_breaks,
										 					 self.context.minor_period_breaks,
										 					 self.context.theme_seaborn_)
		if plots:
			data['notes_created_per_course_sections'] = build_plot_images_dictionary(plots)
		return data

	def get_notes_created_the_most_active_users(self, data):
		plots = self.nctp.plot_the_most_active_users(self.context.number_of_most_active_user)
		if plots:
			data['notes_created_users'] = build_plot_images_dictionary(plots)
		return data

View = NoteEventsTimeseriesReport = NoteEventsTimeseriesReportView
