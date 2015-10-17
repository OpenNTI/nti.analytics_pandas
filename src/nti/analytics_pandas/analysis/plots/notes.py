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
from ggplot import ylab
from ggplot import ylim
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_line
from ggplot import geom_point
from ggplot import date_breaks
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import geom_histogram
from ggplot import scale_x_discrete

from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date

class NotesCreationTimeseriesPlot(object):

	def __init__(self, nct):
		"""
		nct = NotesCreationTimeseries
		"""
		self.nct = nct

	def explore_events(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_notes_created']) + 1
		plot_notes_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_notes_created')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating notes during period of time')) + \
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
				ggtitle(_('Ratio of notes created over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_notes_creation, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_note_created'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_note_created']) + 1
		plot_notes_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_note_created', colour='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes created grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating notes grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes created over unique user grouped by device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return(plot_notes_creation, plot_unique_users, plot_ratio)

	def analyze_resource_types(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_note_created'] / df['number_of_unique_users']

		y_max = pd.Series.max(df['number_of_note_created']) + 1
		plot_notes_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_note_created', colour='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes created grouped by resource type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating notes grouped by resource type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes created over unique user grouped by resource type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_notes_creation, plot_unique_users, plot_ratio)

	def plot_the_most_active_users(self, max_rank_number=10):
		nct = self.nct
		users_df = nct.get_the_most_active_users(max_rank_number)
		if users_df is None :
			return ()

		plot_users = \
				ggplot(users_df, aes(x='username', y='number_of_notes_created')) + \
				geom_histogram(stat="identity") + \
				ggtitle(_('The most active users creating notes')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=15, hjust=1)) + \
				scale_x_discrete('username') + \
				ylab(_('Number of notes created')) + \
				xlab(_('Username'))

		return (plot_users)

	def analyze_sharing_types(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_sharing_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['number_of_note_created']) + 1
		plot_notes_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_note_created', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes created grouped by sharing type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users creating notes grouped by sharing type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes created over unique user grouped by sharing type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return(plot_notes_creation, plot_unique_users, plot_ratio)

class NotesViewTimeseriesPlot(object):

	def __init__(self, nvt):
		"""
		nvt = NotesViewTimeseries
		"""
		self.nvt = nvt

	def explore_events(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_note_views']) + 1
		plot_notes_viewed = \
				ggplot(df, aes(x='timestamp_period', y='total_note_views')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes viewed during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes viewed')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing notes during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes viewed over unique users during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return(plot_notes_viewed, plot_unique_users, plot_ratio)

	def analyze_total_events_based_on_sharing_type(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_sharing_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_notes_viewed']) + 1
		plot_notes_viewed = \
				ggplot(df, aes(x='timestamp_period', y='total_notes_viewed', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes viewed grouped by sharing type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes viewed')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing notes grouped by sharing type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes viewed over unique user grouped by sharing type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return(plot_notes_viewed, plot_unique_users, plot_ratio)

	def plot_the_most_active_users(self, max_rank_number=10):
		nvt = self.nvt
		users_df = nvt.get_the_most_active_users(max_rank_number)
		if users_df is None :
			return ()

		plot_users = \
				ggplot(users_df, aes(x='username', y='number_of_notes_viewed')) + \
				geom_histogram(stat="identity") + \
				ggtitle(_('The most active users viewing notes')) + \
				theme(title=element_text(size=10, face="bold"), axis_text_x=element_text(angle=15, hjust=1)) + \
				scale_x_discrete('username') + \
				ylab(_('Number of notes viewed')) + \
				xlab(_('Username'))

		return (plot_users)

	def analyze_total_events_based_on_device_type(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_device_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_notes_viewed']) + 1
		plot_notes_viewed = \
				ggplot(df, aes(x='timestamp_period', y='total_notes_viewed', colour='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes viewed grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes viewed')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users', colour='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing notes grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes viewed over unique user grouped by device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_notes_viewed, plot_unique_users, plot_ratio)

	def analyze_total_events_based_on_resource_type(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_notes_viewed']) + 1
		plot_notes_viewed = \
				ggplot(df, aes(x='timestamp_period', y='total_notes_viewed', colour='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of notes viewed grouped by resource type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes viewed')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users', colour='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing notes grouped by resource type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='resource_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Ratio of notes viewed over unique user grouped by resource type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_notes_viewed, plot_unique_users, plot_ratio)

	def analyze_unique_events_based_on_sharing_type(self, period_breaks='1 day', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_unique_events_based_on_sharing_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['number_of_unique_notes_viewed']) + 1
		plot_unique_notes_viewed = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_notes_viewed', colour='sharing')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique notes viewed grouped by sharing type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=date_breaks(period_breaks), labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes viewed')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_unique_notes_viewed)


class NoteLikesTimeseriesPlot(object):
	def __init__(self, nlt):
		"""
		nlt = NoteLikesTimeseries
		"""
		self.nlt = nlt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nlt = self.nlt
		df = nlt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_note_likes = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_note_likes',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of note likes'),
				title=_('Number of note likes during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users liking notes during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of note likes over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_note_likes, plot_unique_users, plot_ratio)

class NoteFavoritesTimeseriesPlot(object):
	def __init__(self, nft):
		"""
		nft = NoteFavoritesTimeseries
		"""
		self.nft = nft

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nft = self.nft
		df = nft.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_note_likes = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_note_favorites',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of note favorites'),
				title=_('Number of note favorites during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users voting notes as favorite during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of note favorites over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_note_likes, plot_unique_users, plot_ratio)
		


