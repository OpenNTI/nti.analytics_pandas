#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np
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
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import ggsave

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

		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='total_resource_views')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle('Number of resource views during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks,
							 minor_breaks=minor_period_breaks,
							 labels=date_format("%y-%m-%d")) + \
				ylab('Number of resource views') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle('Number of unique users viewing resource during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks,
							 minor_breaks=minor_period_breaks,
							 labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle('Ratio of resource views over unique user on each available date') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks,
							 minor_breaks=minor_period_breaks,
							 labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date')

		
		return(plot_resource_views, plot_unique_users, plot_ratio)

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


		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of resource views on each resource type') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, 
					labels=date_format("%y-%m-%d")) + \
				ylab('Number of resource views') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of unique users viewing each resource type at given time period') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of unique course resource viewed during time period') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique course resource') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='resource_type')) + \
				geom_point() + \
				ggtitle('Ratio of resource views over unique users grouped by resource type ') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of resource views') + \
				xlab('Date')

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

		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='device_type')) + \
				geom_point() + \
				ggtitle('Number of resource views grouped by device type') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of resource views') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_point() + \
				ggtitle('Number of unique users viewing course resource grouped by device type during time period') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='device_type')) + \
				geom_point() + \
				ggtitle('Number of unique course resource viewed on each device type during time period') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique course resource') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_point() + \
				ggtitle('Ratio of resource views over unique users grouped by device type') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date')

		return (plot_resource_views, plot_unique_users, plot_unique_resources)

	def analyze_events_based_on_resource_device_type(self, period_breaks='1 month', minor_period_breaks='1 week'):
		"""
		plot course resource views based on resource_type type (user agent).
		Group the graphics into different types of user agent (device type)
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_resource_device_type()
		if df is None:
			return ()
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		plot_resource_views = \
				ggplot(df, aes(x='timestamp_period', y='number_of_resource_views', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of resource views using each device type') + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of resource views') + \
				xlab('Date') + \
				facet_wrap('device_type', scales="free")

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of unique users viewing course resource given time period group by device type') + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date') + \
				facet_wrap('device_type', scales="free")

		plot_unique_resources = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_resource', color='resource_type')) + \
				geom_point() + \
				ggtitle('Number of unique course resource viewed on each device type at given time period') + \
				theme(title=element_text(size=8, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique course resource') + \
				xlab('Date') + \
				facet_wrap('device_type', scales="free")

		return (plot_resource_views, plot_unique_users, plot_unique_resources)
