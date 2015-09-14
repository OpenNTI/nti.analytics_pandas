#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryBookmarksCreated

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_
from .common import analyze_types_
from .common import add_timestamp_period

import pandas as pd

class BookmarkCreationTimeseries(object):
	"""
	analyze the number of bookmarks creation given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type=True, with_device_type=True, time_period_date = True):
		self.session = session
		qbc = self.query_bookmarks_created = QueryBookmarksCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qbc.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qbc.filter_by_period_of_time(start_date, end_date)

		if with_resource_type:
			new_df = qbc.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_device_type:
			new_df = qbc.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if time_period_date :
			self.dataframe = add_timestamp_period(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_bookmarks_created'}, inplace=True)
		events_df = events_df[['total_bookmarks_created']]
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_bookmarks_created', unique_users_df)
		return merge_df

	def analyze_resource_types(self):
		group_by_items = ['timestamp_period', 'resource_type']
		agg_columns = {	'bookmark_id' 	: pd.Series.nunique,
						'user_id'		: pd.Series.nunique,
						'device_type'	: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		return df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		agg_columns = {	'bookmark_id' 	: pd.Series.nunique,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		return df

	def analyze_resource_device_types(self):
		group_by_items = ['timestamp_period', 'resource_type', 'device_type']
		agg_columns = {	'bookmark_id' 	: pd.Series.nunique,
						'user_id'		: pd.Series.nunique	}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		return df

