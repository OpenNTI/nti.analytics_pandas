#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryUsers
from ..queries import QueryEntityProfileViews

from ..utils import cast_columns_as_category_
from ..utils import get_values_of_series_categorical_index_

from .common import analyze_types_
from .common import reset_dataframe_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class EntityProfileViewsTimeseries(object):
	"""
	analyze the profile views
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 time_period='daily',
				 with_enrollment_type=True):
		self.session = session
		self.time_period = time_period
		qepv = QueryEntityProfileViews(self.session)

		self.dataframe = qepv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['target_id', 'user_id']
			if with_application_type:
				new_df = qepv.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=time_period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id' 	: pd.Series.count,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_profile_views',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_profile_views'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_profile_views'},
							inplace=True)
		return users_df

	def get_the_most_viewed_profiles(self, max_rank_number=10):
		df = self.dataframe
		if df is None or df.empty:
			return
		most_viewed_profiles_id = df.groupby('target_id').size().sort_values(ascending=False)[:max_rank_number]
		most_viewed_profiles_df = most_viewed_profiles_id.to_frame(name='number_of_profile_viewed')
		most_viewed_profiles_df.reset_index(level=0, inplace=True)

		target_id = get_values_of_series_categorical_index_(most_viewed_profiles_id).tolist()
		target_df = QueryUsers(self.session).get_username_filter_by_user_id(target_id)
		target_df.rename(columns={'user_id' : 'target_id', 'username': 'profile'},
						 inplace=True)

		most_viewed_profiles_df = target_df.merge(most_viewed_profiles_df)

		most_viewed_profiles_df.sort_values(by='number_of_profile_viewed', ascending=[0], inplace=True)
		most_viewed_profiles_df.reset_index(inplace=True, drop=True)
		return most_viewed_profiles_df
