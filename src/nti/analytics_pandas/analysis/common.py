#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

def add_timestamp_period(df, period_format=u'%Y-%m-%d'):
	if 'timestamp' in df.columns:
		df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime(period_format))
	return df

def explore_number_of_events_based_timestamp_date_(df):
	if len(df.index) > 0 :
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		events_df = grouped.aggregate(pd.Series.nunique)
		return events_df

def explore_unique_users_based_timestamp_date_(df):
	if len(df.index) > 0 :
		grouped = df.groupby('timestamp_period')
		unique_users_per_period_df = grouped.aggregate({'user_id' : pd.Series.nunique})
		unique_users_per_period_df.rename(columns={'user_id' : 'total_unique_users'}, inplace=True)
		return unique_users_per_period_df

def explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df,
																	events_df_column_name,
																	unique_users_df):
	if events_df is not None and unique_users_df is not None:
		merge_df = events_df.join(unique_users_df)
		merge_df['ratio'] = merge_df[events_df_column_name] / merge_df['total_unique_users']
		return merge_df

def analyze_types_(df, group_by_items, agg_columns=None):
	if len(df.index) > 0:
		grouped = df.groupby(group_by_items)
		if agg_columns is not None:
			events_df = grouped.aggregate(agg_columns)
		else :
			events_df = grouped.aggregate(pd.Series.nunique)
		return events_df
