#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryHighlightsCreated

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class HighlightsCreationTimeseries(object):
	"""
	analyze the number of highlights creation given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):
		self.session = session
		qhc = self.query_highlights_created = QueryHighlightsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qhc.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qhc.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qhc.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if with_resource_type:
			new_df = qhc.add_resource_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date :
			self.dataframe = add_timestamp_period_(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_highlights_created'}, inplace=True)
			events_df = events_df[['total_highlights_created']]
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_highlights_created', unique_users_df)
		return merge_df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		agg_columns = {	'user_id'	  	: pd.Series.nunique,
						'highlight_id' 	: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={'user_id'		:'number_of_unique_users',
							 'highlight_id'	:'number_of_highlight_created'},
				  inplace=True)
		return df

	def analyze_resource_types(self):
		group_by_items = ['timestamp_period', 'resource_type']
		agg_columns = {	'user_id'	  	: pd.Series.nunique,
						'highlight_id' 	: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={'user_id'		:'number_of_unique_users',
							 'highlight_id'	:'number_of_highlight_created'},
				  inplace=True)
		return df

	def analyze_resource_device_types(self):
		group_by_items = ['timestamp_period', 'resource_type', 'device_type']
		agg_columns = {	'user_id'	  	: pd.Series.nunique,
						'highlight_id' 	: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={'user_id'		:'number_of_unique_users',
							 'highlight_id'	:'number_of_highlight_created'},
				  inplace=True)
		return df
