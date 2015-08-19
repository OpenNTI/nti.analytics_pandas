#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: topics.py 70252 2015-08-10 15:22:32Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.boards import TopicsCreated
from nti.analytics.database.boards import TopicsViewed
from nti.analytics.database.boards import TopicFavorites
from nti.analytics.database.boards import TopicLikes
from nti.analytics_pandas.utils.orm_to_dataframe import orm_dataframe

class QueryTopicsCreated(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date, end_date):
		tc = TopicsCreated
		query = self.session.query(tc.timestamp, tc.user_id, tc.session_id, tc.course_id, tc.topic_ds_id).filter(tc.timestamp.between(start_date, end_date))
		columns = TopicsCreated.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe


class QueryTopicsViewed(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date, end_date):
		tv = TopicsViewed
		query = self.session.query(tv.timestamp, tv.user_id, tv.session_id, tv.course_id, tv.forum_id, tv.topic_id, tv.time_length, tv.context_path).filter(tv.timestamp.between(start_date, end_date))
		columns = TopicsViewed.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe

class QueryTopicFavorites(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date, end_date):
		tf = TopicFavorites
		query = self.session.query(tf.timestamp, tf.session_id, tf.user_id, tf.topic_id, tf.creator_id, tf.course_id).filter(tf.timestamp.between(start_date, end_date))
		columns = TopicFavorites.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe

class QueryTopicLikes(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date, end_date):
		tl = TopicLikes
		query = self.session.query(tl.timestamp, tl.session_id, tl.user_id, tl.topic_id, tl.creator_id, tl.course_id).filter(tl.timestamp.between(start_date, end_date))
		columns = TopicLikes.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe


