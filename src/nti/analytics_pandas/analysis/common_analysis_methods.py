#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: dataframe_operation.py 72535 2015-09-08 15:09:38Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)
import pandas as pd

def add_timestamp_period_date_with_index(df, index_name=None):
	df.set_index(index_name, inplace=True)
	df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d'))
	df.reset_index(inplace=True)
	return df

def add_timestamp_period_date(df):
	df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d'))
	return df

def explore_unique_users_based_timestamp_date_(df):
	df = add_timestamp_period_date(df)
	grouped = df.groupby('timestamp_period')
	unique_users_per_period_df = grouped.agg({'user_id' : pd.Series.nunique})
	unique_users_per_period_df.rename(columns={'user_id' : 'total_unique_users'}, inplace=True)
	return unique_users_per_period_df

def explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, events_df_column_name, unique_users_df):
	merge_df = events_df.join(unique_users_df)
	merge_df['ratio'] = merge_df[events_df_column_name] / merge_df['total_unique_users']
	return merge_df