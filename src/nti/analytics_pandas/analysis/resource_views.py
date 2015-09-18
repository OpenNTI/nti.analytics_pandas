#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

import numpy as np

from ..queries import QueryResources
from ..queries import QueryCourseResourceViews

from ..utils import cast_columns_as_category_
from ..utils import get_values_of_series_categorical_index_

from .common import analyze_types_
from .common import add_timestamp_period
from .common import get_most_active_users_
from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class ResourceViewsTimeseries(object):
	"""
	analyze the number of resource views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):
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

		print(self.dataframe.dtypes)

		categorical_columns = ['resource_id', 'resource_type', 'device_type', 'user_id']
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
		count the number of unique users, number of resource views and number of unique resources in each group
		return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'resource_type']
		df = self.process_analysis_by_type(group_by_columns)
		return df

	def analyze_events_based_on_device_type(self):
		"""
		group course resource views dataframe by timestamp_period and device_type
		count the number of unique users, number of resource views and number of unique resources in each group
		return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.process_analysis_by_type(group_by_columns)
		return df

	def analyze_events_based_on_resource_device_type(self):
		"""
		group course resource views dataframe by timestamp_period, resource_type and device_type
		count the number of unique users, number of resource views and number of unique resources in each group
		return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'resource_type', 'device_type']
		df = self.process_analysis_by_type(group_by_columns)
		return df

	def process_analysis_by_type(self, group_by_columns):
		agg_columns = {	'user_id'			: pd.Series.nunique,
						'resource_view_id' 	: pd.Series.count,
						'resource_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'user_id'	:'number_of_unique_users',
							'resource_view_id'	:'number_of_resource_views',
							'resource_id' : 'number_of_unique_resource'},
					inplace=True)
		##need to reset index to avoid 
		##TODO : check if we can do it without reset_index after updating to pandas 0.17.0
		df.reset_index(inplace=True)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		"""
		find n-most active users, return dataframe having user_id and username columns
		"""
		return get_most_active_users_(self.dataframe, self.session, max_rank_number)

	def get_the_most_viewed_resources(self, max_rank_number=10):
		"""
		find the top n most viewed resources
		return a dataframe with columns : resource_id, resource_display_name, resource_type, and number_of_views
		"""
		temp_df = self.dataframe

		most_views = temp_df.groupby('resource_id').size().order(ascending=False)[:max_rank_number]
		df = most_views.to_frame(name='number_of_views')
		df.reset_index(level=0, inplace=True)

		resources_id = get_values_of_series_categorical_index_(most_views).tolist()
		qr = QueryResources(self.session)
		resource_df = qr.get_resource_display_name_given_id(resources_id)
		resource_df.reset_index(inplace=True, drop=True)

		resource_type_df = temp_df[['resource_id', 'resource_type']][temp_df['resource_id'].isin(resources_id)]
		resource_type_df.drop_duplicates(subset=['resource_id', 'resource_type'], inplace=True)
		resource_type_df.reset_index(inplace=True, drop=True)

		df = df.merge(resource_df).merge(resource_type_df)
		return df

	def analyze_user_activities_on_resource_views(self):
		"""
		analyze how users viewing resources based on resource and device type
		"""
		df = self.dataframe
		group_by_columns = ['timestamp_period', 'user_id', 'resource_type', 'device_type']
		agg_columns = { 'time_length' : [np.mean, np.sum],
						'resource_id' : pd.Series.nunique,
						'resource_view_id' : pd.Series.count}
		result = df.groupby(group_by_columns).aggregate(agg_columns)
		result.reset_index(inplace=True)
		result.rename(columns={	'resource_id' 		: 'number_of_unique_resource',
								'resource_view_id'	: 'number_of_resource_views'},
					inplace=True)
		return result
