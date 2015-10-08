#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: highlights.py 74377 2015-10-08 08:59:13Z egawati.panjei $
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
from ggplot import geom_histogram
from ggplot import geom_line
from ggplot import geom_point
from ggplot import date_format
from ggplot import scale_x_date
from ggplot import scale_x_discrete
from ggplot import element_text
from ggplot import ylim

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
				ggtitle('Number of notes created during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of notes created') + \
				xlab('Date') + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['total_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle('Number of unique users creating notes during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date') + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle('Ratio of notes created over unique user on each available date') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date') + \
				ylim(0, y_max)

		return(plot_notes_creation, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_note_created'] / df['number_of_unique_users']
		print(df.dtypes)

		y_max = pd.Series.max(df['number_of_note_created']) + 1
		plot_notes_creation = \
				ggplot(df, aes(x='timestamp_period', y='number_of_note_created', colour='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle('Number of notes created during grouped by device type period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of notes created') + \
				xlab('Date') + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle('Number of unique users creating notes grouped by device type during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date') + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='device_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle('Ratio of notes created over unique user grouped by device type during time period') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date') + \
				ylim(0, y_max)

		return(plot_notes_creation, plot_unique_users, plot_ratio)

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
				ggtitle('Number of notes created during grouped by resource type period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of notes created') + \
				xlab('Date') + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['number_of_unique_users']) + 1
		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', colour='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle('Number of unique users creating notes grouped by resource type during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date') + \
				ylim(0, y_max)

		y_max = pd.Series.max(df['ratio']) + 1
		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio', colour='resource_type')) + \
				geom_point() + \
				geom_line() + \
				ggtitle('Ratio of notes created over unique user grouped by resource type during time period') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date') + \
				ylim(0, y_max)

		return(plot_notes_creation, plot_unique_users, plot_ratio)
