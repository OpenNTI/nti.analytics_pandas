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

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		y_max = pd.Series.max(df['total_notes_created']) + 1
		plot_notes_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_notes_created')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle(_('Number of notes created during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle(_('Number of unique users creating notes during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle(_('Ratio of notes created over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_notes_creation, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
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
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of notes created during grouped by device type period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of unique users creating notes grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Ratio of notes created over unique user grouped by device type during time period')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		return (plot_notes_creation, plot_unique_users, plot_ratio)

	def analyze_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
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
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of notes created during grouped by resource type period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of notes created')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle(_('Number of unique users creating notes grouped by resource type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date')) + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='resource_type')) + \
				geom_point() + \
				geom_line() + \
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
