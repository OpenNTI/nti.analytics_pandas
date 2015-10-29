#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

import numpy as np

from ..queries import QueryForumsCreated
from ..queries import QueryForumCommentLikes
from ..queries import QueryForumsCommentsCreated
from ..queries import QueryForumCommentFavorites

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_
from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

from ..utils import cast_columns_as_category_

class ForumsEventsTimeseries(object):
	"""
	combine and analyze forums created and comments created, likes, favorites
	"""

	def __init__(self, fct, fcct, fclt, fcft):
		"""
		fct = ForumsCreatedTimeseries
		fcct = ForumsCommentsCreatedTimeseries
		fclt = ForumCommentLikesTimeseries
		fcft = ForumCommentFavoritesTimeseries
		"""
		self.fct = fct
		self.fcct = fcct
		self.fclt = fclt
		self.fcft = fcft

	def combine_all_events_per_date(self):
		"""
		put all topics related events (create, view, like and favorite) into one dataframe
		"""
		fct = self.fct
		fcct = self.fcct
		fclt = self.fclt
		fcft = self.fcft

		forums_created_df = fct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		forum_comments_created_df = fcct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		forum_comment_likes_df = fclt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		forum_comment_favorites_df = fcft.explore_ratio_of_events_over_unique_users_based_timestamp_date()

		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events',
									'total_unique_users', 'ratio', 'event_type'])

		if forums_created_df is not None:
			forums_created_df = self.update_events_dataframe(forums_created_df,
				column_to_rename='total_forums_created', event_type='FORUM CREATED')
			df = df.append(forums_created_df)

		if forum_comments_created_df is not None:
			forum_comments_created_df = self.update_events_dataframe(forum_comments_created_df,
				column_to_rename='total_forums_comments_created', event_type='COMMENTS CREATED')
			df = df.append(forum_comments_created_df)

		if forum_comment_likes_df is not None:
			forum_comment_likes_df = self.update_events_dataframe(forum_comment_likes_df,
				column_to_rename='total_forum_comment_likes', event_type='COMMENT LIKES')
			df = df.append(forum_comment_likes_df)

		if forum_comment_favorites_df is not None:
			forum_comment_favorites_df = self.update_events_dataframe(forum_comment_favorites_df,
				column_to_rename='total_forum_comment_favorites', event_type='COMMENT FAVORITES')
			df = df.append(forum_comment_favorites_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

class ForumsCreatedTimeseries(object):
	"""
	analyze the number of forums created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, time_period_date=True):

		self.session = session
		qfc = self.query_forums_created = QueryForumsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfc.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfc.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qfc.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None:
			events_df.rename(columns={'index':'total_forums_created'}, inplace=True)
			events_df = events_df[['total_forums_created']]
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

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			agg_columns = {	'forum_id'	: pd.Series.nunique,
							'user_id'		: pd.Series.nunique }
			df = analyze_types_(self.dataframe, group_by_items, agg_columns)
			df.rename(columns={	'forum_id'		:'number_of_forums_created',
								'user_id'		:'number_of_unique_users'},
						inplace=True)
			return df

class ForumsCommentsCreatedTimeseries(object):
	"""
	analyze the number of forums comments created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, time_period_date=True):

		self.session = session
		qfcc = self.query_forums_comments_created = QueryForumsCommentsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcc.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcc.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qfcc.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		categorical_columns = ['forum_id', 'parent_user_id', 'device_type', 'user_id']
		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None:
			events_df.rename(columns={'index':'total_forums_comments_created'}, inplace=True)
			events_df = events_df[['total_forums_comments_created']]
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

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			agg_columns = {	'comment_id'	: pd.Series.nunique,
							'user_id'		: pd.Series.nunique,
							'comment_length': np.mean,
							'like_count'	: np.sum,
							'favorite_count': np.sum}
			df = analyze_types_(self.dataframe, group_by_items, agg_columns)
			df.rename(columns={	'comment_id'	 :'number_of_comment_created',
								'user_id'		 :'number_of_unique_users',
								'comment_length' :'average_comment_length'},
					  inplace=True)
			return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities' : 'number_of_comments_created'},
							inplace=True)
		return users_df

class ForumCommentLikesTimeseries(object):
	"""
	analyze the number of forum comment likes given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, time_period_date=True):

		self.session = session
		qfcl = self.query_forum_comment_likes = QueryForumCommentLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcl.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcl.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qfcl.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None:
			events_df.rename(columns={'index':'total_forum_comment_likes'}, inplace=True)
			events_df = events_df[['total_forum_comment_likes']]
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

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_items)
			return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'comment_id'	: pd.Series.count,
						'user_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None :
			df.rename(columns={	'comment_id'	 :'number_of_likes',
								'user_id'		 :'number_of_unique_users'},
					  inplace=True)
			df['ratio'] = df['number_of_likes'] / df['number_of_unique_users']
		return df

class ForumCommentFavoritesTimeseries(object):
	"""
	analyze the number of forum comment favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, time_period_date=True):
		self.session = session
		qfcf = self.query_forum_comment_favorites = QueryForumCommentFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcf.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcf.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qfcf.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None:
			events_df.rename(columns={'index':'total_forum_comment_favorites'}, inplace=True)
			events_df = events_df[['total_forum_comment_favorites']]
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

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_items)
			return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'comment_id'	: pd.Series.count,
						'user_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={	'comment_id'	 :'number_of_favorites',
							'user_id'		 :'number_of_unique_users'},
				  inplace=True)
		df['ratio'] = df['number_of_favorites'] / df['number_of_unique_users']
		return df
