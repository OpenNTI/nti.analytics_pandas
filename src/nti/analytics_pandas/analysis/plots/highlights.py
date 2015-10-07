#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: highlights.py 74263 2015-10-07 03:31:36Z egawati.panjei $
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
from ggplot import geom_line
from ggplot import facet_wrap
from ggplot import geom_point
from ggplot import date_format
from ggplot import scale_x_date
from ggplot import scale_x_discrete
from ggplot import element_text
from ggplot import geom_histogram

class HighlightsCreationTimeseriesPlot(object):

	def __init__(self, hct):
		"""
		hct = HighlightsCreationTimeseries
		"""
		self.hct = hct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		hct = self.hct
		df = hct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None : return
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_highlights_creation = \
				ggplot(df, aes(x='timestamp_period', y='total_highlights_created')) + \
				geom_point(color='orange') + \
				geom_line() + \
				ggtitle('Number of highlights created during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of highlights created') + \
				xlab('Date')

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_point(color='blue') + \
				geom_line() + \
				ggtitle('Number of unique users creating highlights during period of time') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab('Date')

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_point(color='red') + \
				geom_line() + \
				ggtitle('Ratio of highlights created over unique user on each available date') + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Ratio') + \
				xlab('Date')

		return(plot_highlights_creation, plot_unique_users, plot_ratio)