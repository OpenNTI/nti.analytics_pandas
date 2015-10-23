#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: assessments.py 75270 2015-10-22 16:20:26Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

from .commons import histogram_plot
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import facet_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete

class AssignmentViewsTimeseriesPlot(object):

	def __init__(self, avt):
		"""
		avt = AssignmentViewsTimeseries
		"""
		self.avt = avt

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		avt = self.avt
		df = avt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_assignment_views = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_assignments_viewed',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of assignments viewed'),
				title=_('Number of assignments viewed during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users viewing assignments during period of time'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of assignments viewed over unique user on each available date'),
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks)

		return (plot_assignment_views, plot_unique_users, plot_ratio)

	def analyze_events_group_by_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		avt = self.avt
		df = avt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_assignment_views = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_assignments_viewed',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of assignments viewed'),
				title=_('Number of assignments viewed during period of time'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='number_of_unique_users',
				x_axis_label=_('Date'),
				y_axis_label=_('Number of unique users'),
				title=_('Number of unique users viewing assignments during period of time'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(df=df,
				x_axis_field='timestamp_period',
				y_axis_field='ratio',
				x_axis_label=_('Date'),
				y_axis_label=_('Ratio'),
				title=_('Ratio of assignments viewed over unique user on each available date'),
				period_breaks=period_breaks,
				group_by='device_type',
				minor_breaks=minor_period_breaks)

		return (plot_assignment_views, plot_unique_users, plot_ratio)
