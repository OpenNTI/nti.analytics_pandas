#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: topics.py 74846 2015-10-16 02:40:06Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from .commons import group_line_plot_x_axis_date
from .commons import line_plot_x_axis_date

class TopicsCreationTimeseriesPlot(object):

	def __init__(self, tct):
		"""
		hct = TopicsCreationTimeseries
		"""
		self.tct = tct

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None):
		"""
		return plots of topics created during period of time
		it consists of :
			- number of topics created
			- number of unique users
			- ratio of topics created over unique users
		"""
		tct = self.tct
		df = tct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_topics_created = line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='total_topics_created',
				x_axis_label='Date', 
				y_axis_label='Number of topics created', 
				title='Number of topics created during period of time', 
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='total_unique_users',
				x_axis_label='Date', 
				y_axis_label='Number of unique users', 
				title='Number of unique users creating topics during period of time', 
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='ratio',
				x_axis_label='Date', 
				y_axis_label='Ratio', 
				title='Ratio of topics created over unique user on each available date',
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_topics_created, plot_unique_users, plot_ratio)


class TopicViewsTimeseriesPlot(object):

	def __init__(self, tvt):
		"""
		tvt = TopicViewsTimeseries
		"""
		self.tvt = tvt

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None):
		"""
		return plots of topics viewed during period of time
		it consists of :
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_topics_viewed = line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='total_topics_viewed',
				x_axis_label='Date', 
				y_axis_label='Number of topics viewed', 
				title='Number of topics viewed during period of time', 
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='total_unique_users',
				x_axis_label='Date', 
				y_axis_label='Number of unique users', 
				title='Number of unique users viewing topics during period of time', 
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='ratio',
				x_axis_label='Date', 
				y_axis_label='Ratio', 
				title='Ratio of topics viewed over unique user on each available date',
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_topics_viewed, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 day', minor_period_breaks=None):
		"""
		return plots of topics viewed grouped by device type during period of time
		it consists of :
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_topics_viewed = group_line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='number_of_topics_viewed',
				x_axis_label='Date', 
				y_axis_label='Number of topics viewed', 
				title='Number of bookmarks created grouped by device type during period of time', 
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)


		plot_unique_users = group_line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='number_of_unique_users',
				x_axis_label='Date', 
				y_axis_label='Number of unique users', 
				title='Number of unique users viewing topics during period of time', 
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df, 
				x_axis_field='timestamp_period', 
				y_axis_field='ratio',
				x_axis_label='Date', 
				y_axis_label='Ratio', 
				title='Ratio of topics viewed over unique user on each available date', 
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_topics_viewed, plot_unique_users, plot_ratio)


