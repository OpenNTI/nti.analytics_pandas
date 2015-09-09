#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: topics.py 72614 2015-09-09 08:17:26Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import pandas as pd

from ..queries import QueryTopicLikes
from ..queries import QueryTopicsViewed
from ..queries import QueryTopicsCreated
from ..queries import QueryTopicFavorites

from .common_analysis_methods import explore_number_of_events_based_timestamp_date_
from .common_analysis_methods import explore_unique_users_based_timestamp_date_
from .common_analysis_methods import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class TopicsCreationTimeseries(object):
	"""
	analyze the number of topics created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qtc = self.query_topics_created = QueryTopicsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtc.filter_by_period_of_time_and_course_id(start_date, 
																		end_date, 
																		course_id)
		else :
			self.dataframe = qtc.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_topics_created'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, 'total_topics_created', unique_users_df)
		return merge_df

class TopicViewsTimeseries(object):
	"""
	analyze the number of topics viewed given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qtv = self.query_topics_viewed = QueryTopicsViewed(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtv.filter_by_period_of_time_and_course_id(start_date, 
																		end_date, 
																		course_id)
		else :
			self.dataframe = qtv.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_topics_viewed'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, 'total_topics_viewed', unique_users_df)
		return merge_df
