#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory as _

import pandas as pd

import numpy as np

from .commons import generate_plot_names
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date

class VideoEventsTimeseriesPlot(object):

	def __init__(self, vet):
		"""
		vet = VideoEventsTimeseries
		"""
		self.vet = vet

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None,
					   theme_seaborn_=True, video_event_type='watch'):
		"""
		return plots of video events during period of time
		it consists of:
			- number of video events
			- number of unique users
			- ratio of video events over unique users
		"""
		vet = self.vet
		df = vet.analyze_video_events(video_event_type=video_event_type.upper())
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		if video_event_type == 'skip':
			video_event_type = 'skipp'

		event_title = 'Number of videos %sed during period of time' %(video_event_type)
		user_title =  'Number of unique users %sing videos during period of time' %(video_event_type)
		ratio_title = 'Ratio of videos %sed over unique user on each available date' %(video_event_type)
		event_type = 'video_events'
		plots = self.generate_plots(
							df,
							event_title,
							user_title,
							ratio_title,
							period_breaks,
							minor_period_breaks,
							theme_seaborn_,
							event_type)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
					   period_breaks, minor_period_breaks, theme_seaborn_,
					   event_type=None):

		event_name, user_event_name, ratio_event_name = generate_plot_names(event_type)
		plot_video_events = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_video_events',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of videos events'),
								title=event_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_,
								plot_name=event_name)

		plot_unique_users = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=user_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_,
								plot_name=user_event_name)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_,
								plot_name=ratio_event_name)

		return (plot_video_events, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self,
								df,
								group_by,
								event_title,
								user_title,
								ratio_title,
								period_breaks,
								minor_period_breaks,
								theme_seaborn_,
								event_type=None):

		event_name, user_event_name, ratio_event_name = generate_plot_names(event_type)
		plot_video_events = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_video_events',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of videos events'),
									title=event_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name=event_name)

		plot_unique_users = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name=user_event_name)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name=ratio_event_name)

		return (plot_video_events, plot_unique_users, plot_ratio)

	def analyze_video_events_device_types(self, period_breaks='1 week',
										  minor_period_breaks='1 day',
										  video_event_type='WATCH',
										  theme_seaborn_=True):
		"""
		given a video event type (WATCH or SKIP) return plots of video events during period of time
		it consists of:
			- number of video events
			- number of unique users
			- ratio of video events over unique users
		grouped by device types
		"""
		vet = self.vet
		df = vet.analyze_video_events_device_types(video_event_type.upper())
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of video events grouped by device types')
		user_title = _('Number of unique users creating video events grouped by device types')
		ratio_title = _('Ratio of video events over unique users grouped by device types')
		event_type = 'video_events_%s' % (video_event_type.lower())
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_video_events_types(self, period_breaks='1 week',
								   minor_period_breaks='1 day',
								   separate_plot_by_type=True,
								   theme_seaborn_=True):
		"""
		plot video events by video_event_type
		"""
		vet = self.vet
		df = vet.analyze_video_events_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plots = []
		group_by = 'video_event_type'
		event_title = _('Number of video events grouped by event types')
		user_title = _('Number of unique users creating video events grouped by event types')
		ratio_title = _('Ratio of video events over unique users grouped by event types')
		event_type = 'video_events_per_types'
		all_video_events_plots = self.generate_group_by_plots(
													df,
													group_by,
													event_title,
													user_title,
													ratio_title,
													period_breaks,
													minor_period_breaks,
													theme_seaborn_,
													event_type)
		plots.append(all_video_events_plots)

		if separate_plot_by_type:
			video_event_types = np.unique(df['video_event_type'].values.ravel())
			for video_event_type in video_event_types:
				new_df = df[df['video_event_type'] == video_event_type]
				event_title = 'Number of video events (%s)' % (video_event_type)
				user_title = 'Number of unique users  (VIDEO %s)' % (video_event_type)
				ratio_title = 'Ratio of video events over unique user (VIDEO %s)' % (video_event_type)
				event_type = 'video_events_%s' % (video_event_type)
				video_event_plots = self.generate_plots(new_df,
														event_title,
														user_title,
														ratio_title,
														period_breaks,
														minor_period_breaks,
														theme_seaborn_,
														event_type)
				plots.append(video_event_plots)
		return plots

	def analyze_video_events_per_course_sections(self,
												 video_event_type='WATCH',
												 period_breaks='1 week',
												 minor_period_breaks='1 day',
												 theme_seaborn_=True):
		vet = self.vet
		df = vet.analyze_video_events_per_course_sections(video_event_type)
		if df is None:
			return()

		plots = []
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = 'Number of  video events (%s) per course sections' % video_event_type
			user_title = 'Number of unique users per course sections (VIDEO %s)' % video_event_type
			ratio_title = 'Ratio of video events over unique user per course sections (VIDEO %s)' % video_event_type
			event_type = 'video_events_per_course_sections_%s' % (video_event_type)
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_,
															 event_type)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of video events (%s) in %s' % (video_event_type, context_name)
			user_title = 'Number of unique users on video events (%s) in %s' % (video_event_type, context_name)
			ratio_title = 'Ratio of video events (%s) over unique user in %s' % (video_event_type, context_name)
			event_type = 'video_events_%s_in_%s' % (video_event_type, context_name.replace(' ', '_'))
			section_plots = self.generate_plots(
											new_df,
											event_title,
											user_title,
											ratio_title,
											period_breaks,
											minor_period_breaks,
											theme_seaborn_,
											event_type)
			plots.append(section_plots)
		return plots
