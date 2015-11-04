#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

import numpy as np

from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete

class AssessmentEventsTimeseriesPlot(object):

	def __init__(self, aet):
		"""
		aet = AssessmentEventsTimeseries
		"""
		self.aet = aet

	def combine_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		aet = self.aet
		df = aet.combine_events()
		if len(df.index) <= 0:
			return ()
		plot_assessment_events = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='total_events',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of assessments events'),
									title=_('Number of assessments events grouped by event type during period of time'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=_('Number of unique users creating assessments events during period of time'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=_('Ratio of assessments events over unique user on each available date'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks)

		return (plot_assessment_events, plot_unique_users, plot_ratio)

class AssignmentViewsTimeseriesPlot(object):

	def __init__(self, avt):
		"""
		avt = AssignmentViewsTimeseries
		"""
		self.avt = avt

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		avt = self.avt
		df = avt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of assignments viewed during period of time')
		user_title = _('Number of unique users viewing assignments during period of time')
		ratio_title = _('Ratio of assignments viewed over unique user on each available date')
		plots = self.generate_plots(df, event_title, user_title, ratio_title,
									period_breaks, minor_period_breaks)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		avt = self.avt
		df = avt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of assignments viewed per course sections')
			user_title = _('Number of unique users viewing assignments per course sections')
			ratio_title = _('Ratio of assignments viewed over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															group_by,
															event_title,
															user_title,
															ratio_title,
															period_breaks,
															minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of assignments viewed in %s' % (context_name)
			user_title = 'Number of unique users viewing assignments in %s' % (context_name)
			ratio_title = 'Ratio of assignments viewed over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks,
												minor_period_breaks)
			plots.append(section_plots)

		return plots

	def analyze_events_group_by_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		avt = self.avt
		df = avt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of assignments viewed grouped by device types')
		user_title = _('Number of unique users viewing assignments grouped by device types')
		ratio_title = _('Ratio of assignments viewed over unique user grouped by device types')
		plots = self.generate_group_by_plots(df, group_by, event_title, user_title, ratio_title,
											period_breaks, minor_period_breaks)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title, 
						period_breaks, minor_period_breaks):
		plot_assignment_views = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_assignments_viewed',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of assignments viewed'),
									title=event_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks)
		
		return (plot_assignment_views, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title, 
								period_breaks, minor_period_breaks):
		plot_assignment_views = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_assignments_viewed',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of assignments viewed'),
									title=event_title, 
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks)

		return (plot_assignment_views, plot_unique_users, plot_ratio)

class AssignmentsTakenTimeseriesPlot(object):

	def __init__(self, att):
		"""
		att = AssignmentsTakenTimeseries
		"""
		self.att = att

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		att = self.att
		df = att.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of assignments taken during period of time')
		user_title = _('Number of unique users taking assignments during period of time')
		ratio_title = _('Ratio of assignments taken over unique user on each available date')
		plots = self.generate_plots(df, event_title, user_title, ratio_title,
									period_breaks, minor_period_breaks)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		att = self.att
		df = att.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of assignments taken per course sections')
			user_title = _('Number of unique users taking assignments per course sections')
			ratio_title = _('Ratio of assignments taken over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of assignments taken in %s' % (context_name)
			user_title = 'Number of unique users taking assignments in %s' % (context_name)
			ratio_title = 'Ratio of assignments taken over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks,
												minor_period_breaks)
			plots.append(section_plots)

		return plots

	def analyze_events_group_by_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		att = self.att
		df = att.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of assignments taken during period of time')
		user_title = _('Number of unique users taking assignments during period of time')
		ratio_title = _('Ratio of assignments taken over unique user on each available date')
		plots = self.generate_group_by_plots(df, group_by, event_title, user_title, ratio_title,
											period_breaks, minor_period_breaks)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
					   period_breaks, minor_period_breaks):
		
		plot_assignment_taken = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_assignments_taken',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of assignments taken'),
									title=event_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks)

		return(plot_assignment_taken, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
								event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks):
		
		plot_assignment_views = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_assignments_taken',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of assignments taken'),
										title=event_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_users',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of unique users'),
										title=user_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='ratio',
										x_axis_label=_('Date'),
										y_axis_label=_('Ratio'),
										title=ratio_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks)

		return (plot_assignment_views, plot_unique_users, plot_ratio)

	def analyze_assignment_taken_over_total_enrollments(self):
		"""
		TODO : fix plot when there are more than 30 unique values mapped to x
		"""
		att = self.att
		df = att.analyze_assignment_taken_over_total_enrollments()
		df.reset_index(inplace=True)
		plot = histogram_plot_x_axis_discrete(
									df=df,
									x_axis_field='assignment_title' ,
									y_axis_field='ratio',
									x_axis_label=_('Assignments'),
									y_axis_label=_('Ratio'),
									title=_('Ratio of assignments taken over total enrollments'),
									stat='bar')
		return (plot,)

class SelfAssessmentViewsTimeseriesPlot(object):

	def __init__(self, savt):
		"""
		savt =SelfAssessmentViewsTimeseries
		"""
		self.savt = savt

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		savt = self.savt
		df = savt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of self assessments viewed during period of time')
		user_title = _('Number of unique users viewing self assessments during period of time')
		ratio_title = _('Ratio of self assessments viewed over unique user on each available date')
		plots = self.generate_plots(df, event_title, user_title, ratio_title, 
									period_breaks, minor_period_breaks)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		savt = self.savt
		df = savt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of self assessments viewed per course sections')
			user_title = _('Number of unique users viewing self assessments per course sections')
			ratio_title = _('Ratio of self assessments viewed over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of self assessments viewed in %s' % (context_name)
			user_title = 'Number of unique users viewing self assessments in %s' % (context_name)
			ratio_title = 'Ratio of self assessments viewed over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks,
												minor_period_breaks)
			plots.append(section_plots)

		return plots

	def analyze_events_group_by_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		savt = self.savt
		df = savt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of self assessments viewed grouped by device types')
		user_title = _('Number of unique users viewing self assessments grouped by device types')
		ratio_title = _('Ratio of self assessments viewed over unique user grouped by device types')

		plots = self.generate_group_by_plots(df, group_by, 
										event_title, user_title, ratio_title,
										period_breaks, minor_period_breaks)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title, 
					   period_breaks, minor_period_breaks):
		
		plot_self_assessments_views = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_self_assessments_viewed',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of self assessments viewed'),
										title=event_title,
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_users',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of unique users'),
										title=user_title,
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='ratio',
										x_axis_label=_('Date'),
										y_axis_label=_('Ratio'),
										title=ratio_title,
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks)

		return (plot_self_assessments_views, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
								event_title, user_title, ratio_title, 
								period_breaks, minor_period_breaks):
		
		plot_self_assessments_views = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_self_assessments_viewed',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of self assessments viewed'),
											title=event_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_users',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique users'),
											title=user_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='ratio',
											x_axis_label=_('Date'),
											y_axis_label=_('Ratio'),
											title=ratio_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks)

		return (plot_self_assessments_views, plot_unique_users, plot_ratio)


class SelfAssessmentsTakenTimeseriesPlot(object):

	def __init__(self, satt):
		"""
		satt =SelfAssessmentsTakenTimeseries
		"""
		self.satt = satt

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		satt = self.satt
		df = satt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of self assessments taken during period of time')
		user_title = _('Number of unique users taking self assessments during period of time')
		ratio_title = _('Ratio of self assessments taken over unique user on each available date')
		plots = self.generate_plots(df, event_title, user_title, ratio_title,
									period_breaks, minor_period_breaks)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		satt = self.satt
		df = satt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of self assessments taken per course sections')
			user_title = _('Number of unique users taking self assessments per course sections')
			ratio_title = _('Ratio of self assessments taken over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of self assessments taken in %s' % (context_name)
			user_title = 'Number of unique users taking self assessments in %s' % (context_name)
			ratio_title = 'Ratio of self assessments taken over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks,
												minor_period_breaks)
			plots.append(section_plots)	
		return plots

	def analyze_events_group_by_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		satt = self.satt
		df = satt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of self assessments taken grouped by device types')
		user_title = _('Number of unique users taking self assessments grouped by device types')
		ratio_title = _('Ratio of self assessments taken over unique user grouped by device types')
		plots = self.generate_group_by_plots(df, group_by,
											event_title, user_title, ratio_title,
											period_breaks, minor_period_breaks)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks):

		plot_self_assessments_taken = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_self_assessments_taken',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of self assessments taken'),
										title=event_title,
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=user_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		return (plot_self_assessments_taken, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks):
		plot_self_assessments_taken = group_line_plot_x_axis_date(
												df=df,
												x_axis_field='timestamp_period',
												y_axis_field='number_self_assessments_taken',
												x_axis_label=_('Date'),
												y_axis_label=_('Number of self assessments taken'),
												title=event_title,
												period_breaks=period_breaks,
												group_by=group_by,
												minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
												df=df,
												x_axis_field='timestamp_period',
												y_axis_field='number_of_unique_users',
												x_axis_label=_('Date'),
												y_axis_label=_('Number of unique users'),
												title=user_title,
												period_breaks=period_breaks,
												group_by=group_by,
												minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='ratio',
										x_axis_label=_('Date'),
										y_axis_label=_('Ratio'),
										title=ratio_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks)

		return (plot_self_assessments_taken, plot_unique_users, plot_ratio)
