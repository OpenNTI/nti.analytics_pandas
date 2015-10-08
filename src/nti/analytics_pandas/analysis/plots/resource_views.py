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

from ggplot import aes
from ggplot import xlab
from ggplot import ylim
from ggplot import ylab
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_line
from ggplot import facet_wrap
from ggplot import geom_point
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import geom_histogram
from ggplot import scale_x_discrete

class  ResourceViewsTimeseriesPlot(object):

	def __init__(self, rvt):
		"""
		rvt = ResourceViewsTimeseries
		"""
		self.rvt = rvt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of resource views during period of time
		it consists of :
			- number of resource views
			- number of unique users
			- ratio of resource views over unique users
		"""
		rvt = self.rvt
		df = rvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		# datetime.strptime(rvt.start_date, '%Y-%m-%d')
		# datetime.strptime(rvt.end_date, '%Y-%m-%d')

		y_max = pd.Series.max(df['total_resource_views']) + 1
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='total_resource_views')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle(_('Number of resource views during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of resource views')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle(_('Number of unique users viewing resource during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle(_('Ratio of resource views over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_resource_views, plot_unique_users, plot_ratio)

	def analyze_resource_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot resource views based on resource type
		"""
		rvt = self.rvt
		df = rvt.analyze_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True, drop=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_resource_views']) + 1
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of resource views on each resource type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of resource views')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of unique users viewing each resource type at given time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_resource']) + 1
		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of unique course resource viewed during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique course resource')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Ratio of resource views over unique users grouped by resource type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_resource_views, plot_unique_users, plot_unique_resources, plot_ratio)

	def analyze_resource_type_scatter_plot(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot resource views based on resource type
		"""
		rvt = self.rvt
		df = rvt.analyze_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True, drop=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_resource_views']) + 1
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='resource_type')) + \
				geom_point() + \
				ggtitle(_('Number of resource views on each resource type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks,
					labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of resource views')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing each resource type at given time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_resource']) + 1
		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='resource_type')) + \
				geom_point() + \
				ggtitle(_('Number of unique course resource viewed during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique course resource')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='resource_type')) + \
				geom_point() + \
				ggtitle(_('Ratio of resource views over unique users grouped by resource type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_resource_views, plot_unique_users, plot_unique_resources, plot_ratio)

	def analyze_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot course resource views based on device type (user agent)
		"""
		rvt = self.rvt
		df = rvt.analyze_events_based_on_device_type()
		if df is None:
			return ()
		df.reset_index(inplace=True, drop=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_resource_views']) + 1
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of resource views grouped by device type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of resource views')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of unique users viewing course resource grouped by device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_resource']) + 1
		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of unique course resource viewed on each device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique course resource')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Ratio of resource views over unique users grouped by device type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_resource_views, plot_unique_users, plot_unique_resources, plot_ratio)

	def analyze_device_type_scatter_plot(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot course resource views based on device type (user agent)
		"""
		rvt = self.rvt
		df = rvt.analyze_events_based_on_device_type()
		if df is None:
			return ()
		df.reset_index(inplace=True, drop=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_resource_views']) + 1
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='device_type')) + \
				geom_point() + \
				ggtitle(_('Number of resource views grouped by device type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of resource views')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing course resource grouped by device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_resource']) + 1
		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='device_type')) + \
				geom_point() + \
				ggtitle(_('Number of unique course resource viewed on each device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Number of unique course resource')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_point() + \
				ggtitle(_('Ratio of resource views over unique users grouped by device type')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_discrete(labels='timestamp_period') + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_resource_views, plot_unique_users, plot_unique_resources, plot_ratio)

	def analyze_events_based_on_resource_device_type(self, period_breaks='1 month', minor_period_breaks='1 week'):
		"""
		plot course resource views based on resource_type type (user agent).
		Group the graphics into different types of user agent (device type)
		TODO : fix legend and x axis label for faceting
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_resource_device_type()
		if df is None:
			return ()
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']

		pd.Series.max(df['number_of_resource_views']) + 1
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', colour='resource_type')) + \
				geom_point() + \
				ggtitle(_('Number of resource views using each device type')) + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of resource views')) + \
				xlab(_('Date')) + \
				facet_wrap('device_type', scales="free")

		pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='resource_type')) + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing course resource given time period group by device type')) + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				facet_wrap('device_type', scales="free")

		pd.Series.max(df['number_of_unique_resource']) + 1
		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', colour='resource_type')) + \
				geom_point() + \
				ggtitle(_('Number of unique course resource viewed on each device type at given time period')) + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique course resource')) + \
				xlab(_('Date')) + \
				facet_wrap('device_type', scales="free")

		pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='resource_type')) + \
				geom_point() + \
				ggtitle(_('Ratio of resource views over unique users during time period')) + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				facet_wrap('device_type', scales="free")

		return (plot_resource_views, plot_unique_users, plot_unique_resources, plot_ratio)

	def plot_most_active_users(self, max_rank_number=10):
		rvt = self.rvt
		users_df = rvt.get_the_most_active_users(max_rank_number)
		if users_df is None :
			return
		users_df.rename(columns={'number_of_activities' : 'number_of_resource_views'},
						inplace=True)

		plot_users = \
				ggplot(users_df, aes(x='username', y='number_of_resource_views')) + \
				geom_histogram(stat="identity") + \
				ggtitle(_('The most active users viewing resource')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=90, hjust=1)) + \
				scale_x_discrete('username') + \
				ylab(_('Number of resource viewed')) + \
				xlab(_('Username'))

		return (plot_users)
