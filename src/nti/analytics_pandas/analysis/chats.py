#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: bookmarks.py 78428 2015-12-07 15:25:49Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np

import pandas as pd

from ..queries import QueryChatsInitiated
from ..queries import QueryChatsJoined

from ..utils import cast_columns_as_category_

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
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_chats_initiated'},
							inplace=True)
		return users_df
