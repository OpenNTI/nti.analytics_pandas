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

from .commons import group_line_plot_x_axis_date

class ForumsEventsTimeseriesPlot(object):
	
	def __init__(self, fet):
		"""
		fet = ForumsEventsTimeseries
		"""
		self.fet = fet

	def explore_all_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		fet = self.fet
		df = fet.combine_all_events_per_date()
		if len(df.index) <= 0 :
			return ()

		plot_forums_events = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_events',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forums events'),
				title=_('Number of forums events grouped by event type during period of time'),
				period_breaks=period_breaks,
				group_by='event_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating forums events during period of time'),
				period_breaks=period_breaks,
				group_by='event_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forums events over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='event_type',
				minor_breaks=minor_period_breaks)

		return (plot_forums_events, plot_unique_users, plot_ratio)

class ForumsCreatedTimeseriesPlot(object):

	def __init__(self, fct):
		"""
		fct = ForumsCreatedTimeseries
		"""
		self.fct = fct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forums creation during period of time
		it consists of :
			- number of forums creation
			- number of unique users
			- ratio of forums creation over unique users
		"""
		fct = self.fct
		df = fct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_forums_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_forums_created')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of forums created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course catalog views')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating forums during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of forums creation over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date'))

		return (plot_forums_creation, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forums creation grouped by device type during period of time
		it consists of :
			- number of forums creation
			- number of unique users
			- ratio of forums creation over unique users
		"""

		fct = self.fct
		df = fct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_forums_created'] / df['number_of_unique_users']

		plot_forums_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_forums_created', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of forums created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course catalog views')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating forums during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of forums creation over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date'))

		return (plot_forums_creation, plot_unique_users, plot_ratio)

class ForumsCommentsCreatedTimeseriesPlot(object):

	def __init__(self, fcct):
		"""
		fcct = ForumsCommentsCreatedTimeseries
		"""
		self.fcct = fcct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forum comments creation during period of time
		it consists of :
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
		"""
		fcct = self.fcct
		df = fcct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_forums_comments_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_forums_comments_created')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of forums comments created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course catalog views')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating forums comments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of forums comments creation over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date'))

		return (plot_forums_comments_creation, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forum comments creation grouped by device_type during period of time
		it consists of :
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
			- average comment length
		"""
		fcct = self.fcct
		df = fcct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_comment_created'] / df['number_of_unique_users']

		plot_forums_comments_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_comment_created', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of forums comments created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course catalog views')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating forums comments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of forums comments creation over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date'))

		plot_average_comment_length = \
				ggplot(df, aes(x='timestamp_period', y='average_comment_length', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Average forums comments length on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date'))

		return (plot_forums_comments_creation, plot_unique_users, plot_ratio, plot_average_comment_length)

	def plot_the_most_active_users(self, max_rank_number=10):
		fcct = self.fcct
		users_df = fcct.get_the_most_active_users(max_rank_number)
		if users_df is None : return

		plot_users = \
				ggplot(users_df, aes(x='username', y='number_of_comments_created')) + \
				geom_histogram(stat="identity") + \
				ggtitle(_('The most active users by forum comment count')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=90, hjust=1)) + \
				scale_x_discrete('username') + \
				ylab(_('Number of comments')) + \
				xlab('Username')

		return (plot_users,)

class ForumCommentLikesTimeseriesPlot(object):

	def __init__(self, fclt):
		"""
		fclt = ForumCommentLikesTimeseries
		"""
		self.fclt = fclt

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot the number of comments liked on each available date during time period.
		It also shows the number of unique users liking comments
		"""
		fclt = self.fclt
		df = fclt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_comment_likes = \
				ggplot(df, aes(x='timestamp_period', y='number_of_likes', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of comment likes during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Likes count')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users liking forum comments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		return (plot_comment_likes, plot_unique_users)

class ForumCommentFavoritesTimeseriesPlot(object):

	def __init__(self, fcft):
		"""
		fcft = ForumCommentFavoritesTimeseries
		"""
		self.fcft = fcft

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot the number of comment favorites on each available date during time period.
		It also shows the number of unique users adding favorites
		"""
		fcft = self.fcft
		df = fcft.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_comment_favorites = \
				ggplot(df, aes(x='timestamp_period', y='number_of_favorites', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of comment likes during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Favorites count')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users adding favorite to forum comments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		return (plot_comment_favorites, plot_unique_users)
