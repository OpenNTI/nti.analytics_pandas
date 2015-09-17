#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryCourseResourceViews

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_
from .common import add_timestamp_period
from .common import analyze_types_

from ..utils import get_values_of_series_categorical_index_
from ..utils import cast_columns_as_category_

import pandas as pd

class ResourceViewsTimeseries(object):
	"""
	analyze the number of resource views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type=True, with_device_type=True, time_period_date=True):
		self.session = session
		qrv = self.query_resources_view = QueryCourseResourceViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qrv.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qrv.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qrv.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_resource_type:
			new_df = qrv.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if time_period_date :
			self.dataframe = add_timestamp_period(self.dataframe)


		categorical_columns = ['resource_type', 'device_type', 'user_id']
		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_resource_views'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_resource_views', unique_users_df)
		return merge_df

	def analyze_events_based_on_resource_type(self):
		"""
		group course resource views dataframe by timestamp_period and resource_type
		count the number of unique users and unique resource in each group
		return the result as dataframe

		"""
		group_by_items = ['timestamp_period', 'resource_type']
		agg_columns = {	'user_id'			: pd.Series.nunique,
						'resource_view_id' 	: pd.Series.nunique}

		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns = {'user_id'	:'number_of_unique_users',
							 'resource_view_id'	:'number_of_resource_views'}, 
					inplace=True)
		return df



