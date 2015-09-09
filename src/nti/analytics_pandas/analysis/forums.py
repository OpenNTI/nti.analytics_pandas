#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryForumsCreated
from ..queries import QueryForumCommentLikes
from ..queries import QueryForumsCommentsCreated
from ..queries import QueryForumCommentFavorites

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class ForumsCreatedTimeseries(object):
	"""
	analyze the number of forums created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qfc = self.query_forums_created = QueryForumsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfc.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfc.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_forums_created'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_forums_created', unique_users_df)
		return merge_df

class ForumsCommentsCreatedTimeseries(object):
	"""
	analyze the number of forums comments created given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qfcc = self.query_forums_comments_created = QueryForumsCommentsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcc.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcc.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_forums_comments_created'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
									events_df, 'total_forums_comments_created', unique_users_df)
		return merge_df

class ForumCommentLikesTimeseries(object):
	"""
	analyze the number of forum comment likes given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qfcl = self.query_forum_comment_likes = QueryForumCommentLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcl.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcl.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_forum_comment_likes'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_forum_comment_likes', unique_users_df)
		return merge_df

class ForumCommentFavoritesTimeseries(object):
	"""
	analyze the number of forum comment favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qfcf = self.query_forum_comment_favorites = QueryForumCommentFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcf.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcf.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_forum_comment_favorites'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
									events_df, 'total_forum_comment_favorites', unique_users_df)
		return merge_df
