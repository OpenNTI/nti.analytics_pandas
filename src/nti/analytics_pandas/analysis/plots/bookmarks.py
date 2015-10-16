#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from .commons import histogram_plot
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

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None):
		"""
		return scatter plots of bookmarks creation during period of time
		it consists of :
			- number of bookmarks creation
			- number of unique users
			- ratio of bookmark creation over unique users
		"""
		bct = self.bct
		df = bct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_bookmarks_created',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of bookmarks created'),
				title=_('Number of bookmark created during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating bookmarks during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of bookmarks created over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def analyze_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot bookmark creation based on resource type
		"""
		bct = self.bct
		df, resource_df = bct.analyze_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_bookmark_creation',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of bookmarks created'),
				title=_('Number of bookmarks created grouped by resource type during period of time'),
				period_breaks=period_breaks,
				group_by='resource_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label='Number of unique users',
				title=_('Number of unique users creating bookmarks during period of time'),
				period_breaks=period_breaks,
				group_by='resource_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of bookmark creation over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='resource_type',
				minor_breaks=minor_period_breaks)

		resource_df.reset_index(inplace=True)

		plot_total_bookmark_on_each_type = histogram_plot(df=resource_df,
			x_axis_field='resource_type' ,
			y_axis_field='number_of_bookmark_creation',
			x_axis_label=_('Resource Type'),
			y_axis_label=_('Number of bookmarks created'),
			title=_('Number of bookmark creation in each resource type'),
			stat='bar')

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio, plot_total_bookmark_on_each_type)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot bookmark creation based on device type
		"""
		bct = self.bct
		df = bct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_bookmark_creation',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of bookmarks created'),
				title=_('Number of bookmarks created grouped by device type during period of time'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating bookmarks during period of time'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of bookmark creation over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def analyze_resource_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
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

		plot_bookmarks_creation = facet_line_plot_x_axis_date(df=df,
			x_axis_field='timestamp_period',
			y_axis_field='number_of_bookmark_creation',
			x_axis_label=_('Date'),
			y_axis_label=_('Number of resource views'),
			title=_('Number of bookmarks created using each device type grouped by resource types'),
			period_breaks=period_breaks,
			group_by='resource_type',
			facet='device_type',
			minor_breaks=minor_period_breaks,
			scales='free',
			text_size=8)

		plot_unique_users = facet_line_plot_x_axis_date(df=df,
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

		plot_ratio = facet_line_plot_x_axis_date(df=df,
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
		if users_df is None :
			return ()

		plot_users = histogram_plot_x_axis_discrete(df=users_df,
			x_axis_field='username' ,
			y_axis_field='number_of_bookmarks_created',
			x_axis_label=_('Resource Type'),
			y_axis_label=_('Number of bookmarks created'),
			title=_('The most active users creating bookmarks'),
			stat='identity')
		return (plot_users)
