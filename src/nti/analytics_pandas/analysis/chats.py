#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryChatsJoined
from ..queries import QueryChatsInitiated

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class ChatsInitiatedTimeseries(object):
	"""
	analyze the number of chats initiated
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 time_period_date=True,
				 with_enrollment_type=True):
		self.session = session
		qci = QueryChatsInitiated(self.session)

		self.dataframe = qci.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qci.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if time_period_date:
				self.dataframe = add_timestamp_period_(self.dataframe)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'chat_id' 	: pd.Series.nunique,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'chat_id'	:'number_of_chats_initiated',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_chats_initiated'] / df['number_of_unique_users']
			df = reset_dataframe(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_chats_initiated'},
							inplace=True)
		return users_df

class ChatsJoinedTimeseries(object):
	"""
	analyze the number of chats initiated
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 time_period_date=True,
				 with_enrollment_type=True):
		self.session = session
		qcj = QueryChatsJoined(self.session)

		self.dataframe = qcj.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qcj.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if time_period_date:
				self.dataframe = add_timestamp_period_(self.dataframe)

	def get_number_of_users_joining_chat(self):
		group_by_items = ['timestamp_period', 'chat_id']
		df = self.build_dataframe(group_by_items)
		if df is not None:
			df = reset_dataframe(df)
		return df

	def get_application_types_used_to_join_chats(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'user_id'	: pd.Series.count }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id' :'number_of_users_join_chats'},
						inplace=True)
		return df

	def analyze_number_of_users_join_chats_per_date(self):
		df = self.get_number_of_users_joining_chat()
		if df is not None:
			df = df.groupby(['timestamp_period']).agg({'number_of_users_join_chats' :[pd.Series.mean, pd.Series.sum],
													   'chat_id' : pd.Series.nunique})
			df.rename(columns={	'chat_id' :'number_of_chats_created'},
						inplace=True)
			df = reset_dataframe(df)
			return df

	def analyze_unique_users_per_date(self):
		df = self.dataframe.groupby(['timestamp_period']).agg({'user_id' : pd.Series.count})
		if df is not None:
			df.rename(columns={	'user_id' :'number_of_unique_users'},
						inplace=True)
			df = reset_dataframe(df)
		return df

def reset_dataframe(df):
	df.reset_index(inplace=True)
	df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
	return df
