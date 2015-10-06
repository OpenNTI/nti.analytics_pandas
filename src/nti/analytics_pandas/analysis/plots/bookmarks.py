#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ggplot import aes
from ggplot import xlab
from ggplot import ylab
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_line
from ggplot import facet_wrap
from ggplot import geom_point
from ggplot import date_format
from ggplot import scale_x_date
from ggplot import element_text
from ggplot import geom_histogram

class BookmarksTimeseriesPlot(object):
	def __init__(self, bct):
		"""
		bct = BookmarkCreationTimeseries
		"""
		self.bct = bct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of bookmarks creation during period of time
		it consists of :
			- number of bookmarks creation
			- number of unique users
			- ratio of bookmark creation over unique users
		"""
		bct = self.bct
		df = bct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None : return
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_bookmarks_created')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle('Number of bookmark creation during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of bookmark creation') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle('Number of unique users creating bookmarks during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle('Ratio of bookmark creation over unique user on each available date') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date')

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def analyze_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot bookmark creation based on resource type
		"""
		bct = self.bct
		df, resource_df = bct.analyze_resource_types()
		if df is None : return
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_bookmark_creation', color='resource_type')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle('Number of bookmark creation during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of bookmark creation') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle('Number of unique users creating bookmarks during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='resource_type')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle('Ratio of bookmark creation over unique user on each available date') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date')

		resource_df.reset_index(inplace=True)
		plot_total_bookmark_on_each_type = \
				ggplot(resource_df, aes(x='resource_type', y='number_of_bookmark_creation')) + \
				geom_histogram(stat="bar") + \
				ggtitle('Number of bookmark creation on each resource type') + \
				theme(title=element_text(size=10, face="bold")) + \
				ylab('Number of bookmark creation') + \
				xlab('Resource type')

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio, plot_total_bookmark_on_each_type)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot bookmark creation based on device type
		"""
		bct = self.bct
		df = bct.analyze_device_types()
		if df is None : return
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_bookmark_creation', color='device_type')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle('Number of bookmark creation during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of bookmark creation') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle('Number of unique users creating bookmarks during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle('Ratio of bookmark creation over unique user on each available date') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date')

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)

	def analyze_resource_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		Plot bookmark creation based on resource type.
		Show scatter plot of all types of user agent (device type)
		##TODO : fix legend for resource_type
		"""
		bct = self.bct
		df = bct.analyze_resource_device_types()
		if df is None : return
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_bookmarks_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_bookmark_creation', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of bookmark creation using each device type') + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of resource views') + \
				xlab('Date') + \
				facet_wrap('device_type', scales="free")

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of unique users creating bookmarks during time period group by device type') + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date') + \
				facet_wrap('device_type', scales="free")

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='resource_type')) + \
				geom_point() + \
				ggtitle('Ratio of bookmark creation over unique user on each available date') + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date') + \
				facet_wrap('device_type', scales="free")

		return (plot_bookmarks_creation, plot_unique_users, plot_ratio)
