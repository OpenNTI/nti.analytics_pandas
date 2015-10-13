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
