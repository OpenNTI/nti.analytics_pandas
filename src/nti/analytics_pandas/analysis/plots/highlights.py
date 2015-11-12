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

from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete
from .commons import generate_plot_names

class HighlightsCreationTimeseriesPlot(object):

	def __init__(self, hct):
		"""
		hct = HighlightsCreationTimeseries
		"""
		self.hct = hct

	def explore_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day', theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of highlights created during period of time')
		user_title = _('Number of unique users created highlights during period of time')
		ratio_title = _('Ratio of highlights created over unique users during period of time')
		event_type = 'highlights_created'
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of highlights created per course sections')
			user_title = _('Number of unique users creating highlights per course sections')
			ratio_title = _('Ratio of highlights created over unique user per course sections')
			event_type = 'highlights_created_per_course_sections'
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
			event_title = 'Number of highlights created in %s' % (context_name)
			user_title = 'Number of unique users creating highlights in %s' % (context_name)
			ratio_title = 'Ratio of highlights created over unique user in %s' % (context_name)
			event_type = 'highlights_created_in_%s' %(context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
			plots.append(section_plots)
		return plots

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of highlights created grouped by device types')
		user_title = _('Number of unique users created highlights grouped by device types')
		ratio_title = _('Ratio of highlights created over unique users grouped by device types')
		event_type = 'highlights_created_per_device_types'
		plots = self.generate_group_by_plots(df,
											 group_by,
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
		plot_highlights_created = line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_highlights_created',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of highlights created'),
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

		return (plot_highlights_created, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks, theme_seaborn_,
								event_type=None):
		event_name, user_event_name, ratio_event_name = generate_plot_names(event_type)
		plot_highlights_created = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_highlights_created',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of highlights created'),
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

		return (plot_highlights_created, plot_unique_users, plot_ratio)

	def analyze_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day',
								theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'resource_type'
		event_title = _('Number of highlights created grouped by resource types')
		user_title = _('Number of unique users created highlights grouped by resource types')
		ratio_title = _('Ratio of highlights created over unique users grouped by resource types')
		event_type = 'highlights_created_per_resource_types'
		plots = self.generate_group_by_plots(df, group_by,
											event_title, user_title, ratio_title,
											period_breaks, minor_period_breaks,
											theme_seaborn_, event_type)

		return plots

	def plot_the_most_active_users(self, max_rank_number=10):
		hct = self.hct
		users_df = hct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_highlights_created',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of highlights created'),
											title=_('The most active users creating highlights'),
											stat='identity',
											plot_name='most_active_users_creating_highlights')
		return (plot_users,)
