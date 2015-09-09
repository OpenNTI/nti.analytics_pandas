#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryTopicLikes
from ..queries import QueryTopicsViewed
from ..queries import QueryTopicsCreated
from ..queries import QueryTopicFavorites

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

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
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_topics_created', unique_users_df)
		return merge_df

class TopicLikesTimeseries(object):
	"""
	analyze the number of topic likes given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qtl = self.query_topic_likes = QueryTopicLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtl.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qtl.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_topic_likes'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
												events_df, 'total_topic_likes', unique_users_df)
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
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_topics_viewed', unique_users_df)
		return merge_df

class TopicFavoritesTimeseries(object):
	"""
	analyze the number of topic favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qtf = self.query_topic_favorites = QueryTopicFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtf.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qtf.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_topic_favorites'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_topic_favorites', unique_users_df)
		return merge_df
