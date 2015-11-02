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

from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete

class ForumsEventsTimeseriesPlot(object):

	def __init__(self, fet):
		"""
		fet = ForumsEventsTimeseries
		"""
		self.fet = fet

	def explore_all_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		fet = self.fet
		df = fet.combine_all_events_per_date()
		if len(df.index) <= 0:
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
		it consists of:
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

		plot_forums_created = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_forums_created',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forums created'),
				title=_('Number of forums created during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating forums during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forums created over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_forums_created, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forums creation grouped by device type during period of time
		it consists of:
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

		plot_forums_created = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_forums_created',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forums created'),
				title=_('Number of forums created grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating forums grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forums created over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_forums_created, plot_unique_users, plot_ratio)

class ForumsCommentsCreatedTimeseriesPlot(object):

	def __init__(self, fcct):
		"""
		fcct = ForumsCommentsCreatedTimeseries
		"""
		self.fcct = fcct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forum comments creation during period of time
		it consists of:
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

		plot_forum_comments_created = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_forums_comments_created',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forum comments created'),
				title=_('Number of forums created during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating forum comments during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forums comments created over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_forum_comments_created, plot_unique_users, plot_ratio)

	def analyze_comments_per_section(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forum comments creation grouped by device_type during period of time
		it consists of:
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
			- average comment length
		"""
		fcct = self.fcct
		df = fcct.analyze_comments_per_section()
		if df is None:
			return()
		

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of forum comments creation grouped by device_type during period of time
		it consists of:
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


		plot_forum_comments_created = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_comment_created',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forum comments created'),
				title=_('Number of forum comments created grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating forum comments grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forums comments created over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_average_comment_length = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='average_comment_length',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Average forums comments length on each available date'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_forum_comments_created, plot_unique_users, plot_ratio, plot_average_comment_length)

	def plot_the_most_active_users(self, max_rank_number=10):
		fcct = self.fcct
		users_df = fcct.get_the_most_active_users(max_rank_number)
		if users_df is None: return

		plot_users = histogram_plot_x_axis_discrete(df=users_df,
			x_axis_field='username' ,
			y_axis_field='number_of_comments_created',
			x_axis_label=_('Username'),
			y_axis_label=_('Number of comments'),
			title=_('The most active users by forum comment count'),
			stat='identity')

		return (plot_users,)

class ForumCommentLikesTimeseriesPlot(object):

	def __init__(self, fclt):
		"""
		fclt = ForumCommentLikesTimeseries
		"""
		self.fclt = fclt

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return plots of forum comment likes during period of time
		it consists of:
			- number of forums comment likes
			- number of unique users
			- ratio of forum comment likes over unique users
		"""
		fclt = self.fclt
		df = fclt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_comment_likes = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_likes',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forum comment likes'),
				title=_('Number of forums comment likes during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users liking forum comments during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forum comments liked over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_comment_likes, plot_unique_users, plot_ratio)

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

		plot_comment_likes = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_likes',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forum comment likes'),
				title=_('Number of forum comments likes grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users liking forum comments grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forum comments liked over unique user grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_comment_likes, plot_unique_users, plot_ratio)

class ForumCommentFavoritesTimeseriesPlot(object):

	def __init__(self, fcft):
		"""
		fcft = ForumCommentFavoritesTimeseries
		"""
		self.fcft = fcft

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return plots of forum comment favorites during period of time
		it consists of:
			- number of forums comment favorites
			- number of unique users
			- ratio of forum comment favorites over unique users
		"""
		fcft = self.fcft
		df = fcft.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_comment_favorites = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_favorites',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forum comment favorites'),
				title=_('Number of forums comment favorites during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users voting forum comments as favorites during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of forum comment favorites over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_comment_favorites, plot_unique_users, plot_ratio)

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

		plot_comment_favorites = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_favorites',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of forum comment favorites'),
				title=_('Number of forum comments likes grouped by device types'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users voting forum comments as favorites during period of time'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_comment_favorites, plot_unique_users)
