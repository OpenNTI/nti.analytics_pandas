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

from .commons import histogram_plot
from .commons import generate_plot_names
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import facet_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete

class BookmarksTimeseriesPlot(object):

	def __init__(self, bct):
		"""
		bct = BookmarkCreationTimeseries
		"""
		self.bct = bct

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None,
					   theme_seaborn_=True):
		"""
		return scatter plots of bookmarks creation during period of time
		it consists of:
			- number of bookmarks creation
			- number of unique users
			- ratio of bookmark creation over unique users
		"""
		bct = self.bct
		df = bct.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of bookmarks created during period of time')
		user_title = _('Number of unique users creating bookmarks during period of time')
		ratio_title = _('Ratio of bookmarks created over unique user on each available date')
		event_type = 'bookmarks_created'
		plots = self.generate_plots(df,
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
		plot_bookmarks_creation = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_bookmarks_created',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of bookmarks created'),
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

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def analyze_events_per_course_sections(self, period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		bct = self.bct
		df = bct.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of bookmarks created per course sections')
			user_title = _('Number of unique users creating bookmarks per course sections')
			ratio_title = _('Ratio of bookmarks created over unique user per course sections')
			event_type = 'bookmarks_created_per_course_sections'
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
			event_title = 'Number of bookmarks created in %s' % (context_name)
			user_title = 'Number of unique users creating bookmarks in %s' % (context_name)
			ratio_title = 'Ratio of bookmarks created over unique user in %s' % (context_name)
			event_type = 'bookmarks_created_in_%s' % (context_name.replace(' ', ''))
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

	def analyze_resource_types(self, period_breaks='1 week',
							   minor_period_breaks='1 day',
							   theme_seaborn_=True):
		"""
		plot bookmark creation based on resource type
		"""
		bct = self.bct
		df, resource_df = bct.analyze_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'resource_type'
		event_title = _('Number of bookmarks created grouped by resource types')
		user_title = _('Number of unique users creating bookmarks  grouped by resource types')
		ratio_title = _('Ratio of bookmarks created over unique user grouped by resource types')
		event_type = 'bookmarks_created_per_resource_types'
		
		plots_dict = {}
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_,
											 event_type)
		plots_dict['line_plots'] = plots

		resource_df.reset_index(inplace=True)

		plot_total_bookmark_on_each_type = histogram_plot(
												df=resource_df,
												x_axis_field='resource_type' ,
												y_axis_field='number_of_bookmarks_created',
												x_axis_label=_('Resource Type'),
												y_axis_label=_('Number of bookmarks created'),
												title=_('Number of bookmarks created in each resource type'),
												stat='bar',
												plot_name='bookmarks_created_per_resource_types_hist')

		plots_dict['hist_plot'] = plot_total_bookmark_on_each_type
		return plots_dict

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):
		"""
		plot bookmark creation based on device type
		"""
		bct = self.bct
		df = bct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of bookmarks created grouped by device types')
		user_title = _('Number of unique users creating bookmarks  grouped by device types')
		ratio_title = _('Ratio of bookmarks created over unique user grouped by device types')
		event_type = 'bookmarks_created_per_device_types'
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

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks, theme_seaborn_,
								event_type=None):

		event_name, user_event_name, ratio_event_name = generate_plot_names(event_type)
		plot_bookmarks_creation = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_bookmarks_created',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of bookmarks created'),
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

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def analyze_resource_device_types(self, period_breaks='1 week', minor_period_breaks='1 day',):
		"""
		Plot bookmark creation based on resource type.
		Show scatter plot of all types of user agent (device type)
		# TODO: fix legend for resource_type
		"""

		bct = self.bct
		df = bct.analyze_resource_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = facet_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_bookmarks_created',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of resource views'),
											title=_('Number of bookmarks created using each device type grouped by resource types'),
											period_breaks=period_breaks,
											group_by='resource_type',
											facet='device_type',
											minor_breaks=minor_period_breaks,
											scales='free',
											text_size=8)

		plot_unique_users = facet_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_users',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique users'),
											title=_('Number of unique users creating bookmarks grouped by resource types during time period'),
											period_breaks=period_breaks,
											group_by='resource_type',
											facet='device_type',
											minor_breaks=minor_period_breaks,
											scales='free',
											text_size=8)

		plot_ratio = facet_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='ratio',
											x_axis_label=_('Date'),
											y_axis_label=_('Ratio'),
											title=_('Ratio of bookmark creation over unique user on each available date'),
											period_breaks=period_breaks,
											group_by='resource_type',
											facet='device_type',
											minor_breaks=minor_period_breaks,
											scales='free',
											text_size=8)

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def plot_the_most_active_users(self, max_rank_number=10):

		bct = self.bct
		users_df = bct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_bookmarks_created',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of bookmarks created'),
											title=_('The most active users creating bookmarks'),
											stat='identity',
											plot_name='most_active_user_creating_bookmarks')
		return (plot_users,)
