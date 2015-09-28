#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *

class  ResourceViewsTimeseriesPlot(object):

	def __init__(self, rvt):
		"""
		rvt = ResourceViewsTimeseries
		"""
		self.rvt = rvt

	def explore_events(self):
		"""
		return scatter plots of resource views during period of time
		it consists of :
			- number of resource views
			- number of unique users
			- ratio of resource views over unique users
		"""
		rvt = self.rvt
		df = rvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		plot_resource_views = ggplot(df, aes(x='timestamp_period', y='total_resource_views')) + \
					geom_point(color = 'orange') + \
					ggtitle('Number of resource views during period of time') + \
					scale_x_date(labels='%Y-%m-%d', breaks=date_breaks('1 week')) + \
					ylab('Number of resource views') + \
					xlab('Date')
		plot_unique_users = ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
					geom_point(color = 'blue') + \
					ggtitle('Number of unique users viewing resource during period of time') + \
					scale_x_date(labels='%Y-%m-%d', breaks=date_breaks('1 week')) + \
					ylab('Number of resource views') + \
					xlab('Date')
		plot_ratio = ggplot(df, aes(x='timestamp_period', y='ratio')) + \
					geom_point(color = 'red') + \
					ggtitle('Ratio of resource views over unique user on each available date') + \
					scale_x_date(labels='%b%d', breaks=date_breaks('1 week')) + \
					ylab('Ratio') + \
					xlab('Date')
		#ggsave(plot_resource_views, 'resource_views.png')
		#ggsave(plot_unique_users, 'unique_users.png')
		#ggsave(plot_ratio, 'ratio.png')
		return plot_resource_views, plot_unique_users, plot_ratio
