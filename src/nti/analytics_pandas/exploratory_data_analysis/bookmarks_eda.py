#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"


from ..queries.bookmarks import QueryBookmarksCreated
import pandas as pd

class BookmarkCreationTimeseries(object):
	"""
	analyze the number of bookmarks creation given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		self.query_bookmarks_created = QueryBookmarksCreated(self.session)
		qbc = self.query_bookmarks_created
		if isinstance (course_id, list):
			self.dataframe = qbc.filter_by_course_id_and_period_of_time(start_date, end_date, course_id)
		else :
			self.dataframe = qbc.filter_by_period_of_time(start_date,end_date)

	def add_timestamp_period_date(self):
		df = self.dataframe
		df.set_index('bookmark_id', inplace=True)
		df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d'))
		df.reset_index(inplace=True)
		return df

	def explore_number_of_events_based_timestamp_date(self):
		df = self.add_timestamp_period_date()
		grouped = df.groupby('timestamp_period')
		timestamp_period_df = grouped.agg({'bookmark_id' : pd.Series.nunique})
		timestamp_period_df.rename(columns = {'bookmark_id':'total_bookmarks_created'}, inplace=True)
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
		merge_df['ratio'] = merge_df['total_bookmarks_created']/merge_df['total_unique_users']
		return merge_df

