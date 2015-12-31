#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: chats.py 78936 2015-12-14 16:33:56Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryContactsAdded
from ..queries import QueryContactsRemoved

from ..queries import QueryDynamicFriendsListsCreated
from ..queries import QueryDynamicFriendsListsMemberAdded
from ..queries import QueryDynamicFriendsListsMemberRemoved

from ..queries import QueryFriendsListsCreated
from ..queries import QueryFriendsListsMemberAdded
from ..queries import QueryFriendsListsMemberRemoved
from .common import analyze_types_
from .common import reset_dataframe_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class ContactsAddedTimeseries(object):
	"""
	analyze the number of contacts added
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 time_period='daily'):
		self.session = session
		self.time_period = time_period
		qca = QueryContactsAdded(self.session)

		self.dataframe = qca.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qca.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=time_period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id' : pd.Series.count,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_contacts_added',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_contacts_added'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_contacts_added'},
							inplace=True)
		return users_df

class ContactsRemovedTimeseries(object):
	"""
	analyze the number of contacts removed
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 time_period='daily'):
		self.session = session
		self.time_period = time_period
		qcr = QueryContactsRemoved(self.session)

		self.dataframe = qcr.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qcr.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=time_period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id' : pd.Series.count,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_contacts_removed',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_contacts_removed'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_contacts_removed'},
							inplace=True)
		return users_df