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

from ggplot import aes
from ggplot import xlab
from ggplot import ylab
from ggplot import ylim
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_line
from ggplot import geom_point
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import geom_histogram
from ggplot import scale_x_discrete

class HighlightsCreationTimeseriesPlot(object):

	def __init__(self, hct):
		"""
		hct = HighlightsCreationTimeseries
		"""
		self.hct = hct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		hct = self.hct
		df = hct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_highlights_created']) + 1
		plot_highlights_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_highlights_created')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of highlights created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of highlights created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating highlights during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of highlights created over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_highlights_creation, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		hct = self.hct
		df = hct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_highlight_created'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_highlight_created']) + 1
		plot_highlights_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_highlight_created', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of highlights created  using each device type')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=45, hjust=1)) + \
				scale_x_date(labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of highlights created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating highlights using each device types during time period')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=45, hjust=1)) + \
				scale_x_date(labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of highlights created over unique users grouped by device type')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=45, hjust=1)) + \
				scale_x_date(labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_highlights_creation, plot_unique_users, plot_ratio)

	def analyze_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		hct = self.hct
		df = hct.analyze_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_highlight_created'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_highlight_created']) + 1
		plot_highlights_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_highlight_created', color='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of highlights created grouped by resource type')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=45, hjust=1)) + \
				scale_x_date(labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of highlights created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating highlights grouped by resource type during time period')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=45, hjust=1)) + \
				scale_x_date(labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of highlights created over unique users grouped by resource type')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=45, hjust=1)) + \
				scale_x_date(labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_highlights_creation, plot_unique_users, plot_ratio)

	def plot_the_most_active_users(self, max_rank_number=10):
		hct = self.hct
		users_df = hct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = \
				ggplot(users_df, aes(x='username', y='number_of_highlights_created')) + \
				geom_histogram(stat="identity") + \
				ggtitle(_('The most active users creating highlights')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=15, hjust=1)) + \
				scale_x_discrete('username') + \
				ylab(_('Number of highlights created')) + \
				xlab(_('Username'))

		return (plot_users,)
