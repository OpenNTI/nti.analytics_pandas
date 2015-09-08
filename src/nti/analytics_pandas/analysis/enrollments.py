#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import pandas as pd

from ..queries.enrollments import QueryCourseCatalogViews

class CourseCatalogViewsTimeseries(object):
	"""
	analyze the number of course catalog views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qccv = self.query_course_catalog_views = QueryCourseCatalogViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qccv.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qccv.filter_by_period_of_time(start_date, end_date)

	def add_timestamp_period_date(self):
		df = self.dataframe
		df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d'))
		return df

	def explore_number_of_events_based_timestamp_date(self):
		df = self.add_timestamp_period_date()
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		timestamp_period_df = grouped.aggregate(pd.Series.nunique)
		timestamp_period_df.rename(columns = {'index':'total_course_catalog_views'}, inplace=True)
		return timestamp_period_df

	def explore_unique_users_based_timestamp_date(self):
		df = self.add_timestamp_period_date()
		grouped = df.groupby('timestamp_period')
		unique_users_per_period_df = grouped.agg({'user_id' : pd.Series.nunique})
		unique_users_per_period_df.rename(columns = {'user_id' : 'total_unique_users'}, inplace=True)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = events_df.join(unique_users_df)
		merge_df['ratio'] = merge_df['total_course_catalog_views']/merge_df['total_unique_users']
		return merge_df
