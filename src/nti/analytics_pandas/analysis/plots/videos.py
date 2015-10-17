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

class VideoEventsTimeseriesPlot(object):

	def __init__(self, vet):
		"""
		vet = VideoEventsTimeseries
		"""
		self.vet = vet

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None):
		"""
		return plots of video events during period of time
		it consists of :
			- number of video events
			- number of unique users
			- ratio of video events over unique users
		"""
		vet = self.vet
		df = vet.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_video_events = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_video_events',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of videos watched and skipped'),
				title=_('Number of videos watched and skipped during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='total_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users watching or skipping videos during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of videos watched and skipped over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_video_events, plot_unique_users, plot_ratio)

	def analyze_video_events_types(self, period_breaks='1 week', minor_period_breaks='1 day', separate_plot_by_type=True):
		"""
		plot video events  by video_event_type
		"""
		vet = self.vet
		df = vet.analyze_video_events_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		if separate_plot_by_type:
			watch_df = df.loc[df['video_event_type'] == 'WATCH']
			watch_plots = self.generate_plots_video_events(watch_df, period_breaks, minor_period_breaks, 'watched')
			skip_df = df.loc[df['video_event_type'] == 'SKIP']
			skip_plots = self.generate_plots_video_events(skip_df, period_breaks, minor_period_breaks, 'skipped')
			return (watch_plots, skip_plots)
		else:
			return self.generate_plots_grouped_by_video_event_types(df, period_breaks, minor_period_breaks)

	def generate_plots_grouped_by_video_event_types(self, df, period_breaks, minor_period_breaks):

		plot_video_events = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_video_events',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of video events'),
				title=_('Number of video events grouped by resource type during period of time'),
				period_breaks=period_breaks,
				group_by='video_event_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users creating video events during period of time'),
				period_breaks=period_breaks,
				group_by='video_event_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of video events over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='video_event_type',
				minor_breaks=minor_period_breaks)

		return (plot_video_events, plot_unique_users, plot_ratio)

	def generate_plots_video_events(self, df, period_breaks, minor_period_breaks, event_type):
		title = _("Number of video ${event_type} during period of time",
				 mapping={'event_type' : event_type })
		plot_video_events = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_video_events',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of video events'),
				title=title,
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		title = _("Number of unique users who ${event_type} video during period of time",
				 mapping={'event_type' : event_type })
		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=title,
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		title = _("Ratio of video ${event_type} over unique user on each available date",
				 mapping={'event_type' : event_type })
		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=title,
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_video_events, plot_unique_users, plot_ratio)
