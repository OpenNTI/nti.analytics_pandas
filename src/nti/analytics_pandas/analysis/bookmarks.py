#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np

import pandas as pd

from ..queries import QueryBookmarksCreated

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import add_timestamp_period
from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_
from .common import get_most_active_users_

class BookmarkCreationTimeseries(object):
	"""
	analyze the number of bookmarks creation given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):

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

		categorical_columns = ['bookmark_id', 'user_id', 'device_type', 'resource_type']
		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

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
		df = self.process_analysis_by_type(group_by_items)
		resource_df = df[['number_of_bookmark_creation']]
		resource_df.reset_index(inplace=True)
		grouped = resource_df.groupby(['resource_type'])
		resource_df = grouped.aggregate({'number_of_bookmark_creation' : np.sum})
		return df, resource_df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.process_analysis_by_type(group_by_items)
		return df

	def process_analysis_by_type(self, group_by_columns):
		agg_columns = {	'bookmark_id' 	: pd.Series.nunique,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'bookmark_id'	:'number_of_bookmark_creation',
							'user_id'		:'number_of_unique_users'},
					inplace=True)
		df['ratio'] = df['number_of_bookmark_creation'] / df['number_of_unique_users']
		return df

	def analyze_resource_device_types(self):
		group_by_items = ['timestamp_period', 'resource_type', 'device_type']
		df = self.process_analysis_by_type(group_by_items)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None :
			users_df.rename(columns={'number_of_activities' : 'number_of_bookmarks_created'},
							inplace=True)
		return users_df
