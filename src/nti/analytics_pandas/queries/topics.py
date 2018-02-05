#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.analytics_database.boards import TopicLikes
from nti.analytics_database.boards import TopicsViewed
from nti.analytics_database.boards import TopicsCreated
from nti.analytics_database.boards import TopicFavorites

from nti.analytics_pandas.queries.mixins import TableQueryMixin

from nti.analytics_pandas.queries.common import add_device_type_
from nti.analytics_pandas.queries.common import add_context_name_

from nti.analytics_pandas.queries.enrollments import add_enrollment_type_

from nti.analytics_pandas.utils import orm_dataframe

logger = __import__('logging').getLogger(__name__)


class QueryTopicsCreated(TableQueryMixin):

    table = TopicsCreated

    def filter_by_period_of_time(self, start_date, end_date):
        tc = self.table
        query = self.session.query(tc.timestamp,
                                   tc.deleted,
                                   tc.favorite_count,
                                   tc.is_flagged,
                                   tc.like_count,
                                   tc.topic_id,
                                   tc.user_id,
                                   tc.session_id,
                                   tc.topic_ds_id,
                                   tc.forum_id,
                                   tc.entity_root_context_id,
                                   tc.root_context_id.label('course_id'))
        query = query.filter(tc.timestamp.between(start_date, end_date))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def filter_by_period_of_time_and_course_id(self, start_date, end_date, course_id=()):
        tc = self.table
        query = self.session.query(tc.timestamp,
                                   tc.deleted,
                                   tc.favorite_count,
                                   tc.is_flagged,
                                   tc.like_count,
                                   tc.topic_id,
                                   tc.user_id,
                                   tc.session_id,
                                   tc.topic_ds_id,
                                   tc.forum_id,
                                   tc.entity_root_context_id,
                                   tc.root_context_id.label('course_id'))
        query = query.filter(tc.timestamp.between(start_date, end_date)).filter(tc.root_context_id.in_(course_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def add_device_type(self, dataframe):
        new_df = add_device_type_(self.session, dataframe)
        return new_df

    def add_context_name(self, dataframe, course_id):
        new_df = add_context_name_(self.session, dataframe, course_id)
        return new_df

    def add_enrollment_type(self, dataframe, course_id):
        new_df = add_enrollment_type_(self.session, dataframe, course_id)
        return new_df


class QueryTopicsViewed(TableQueryMixin):

    table = TopicsViewed

    def filter_by_period_of_time(self, start_date, end_date):
        tv = self.table
        query = self.session.query(tv.timestamp,
                                   tv.user_id,
                                   tv.session_id,
                                   tv.root_context_id.label('course_id'),
                                   tv.forum_id,
                                   tv.topic_id,
                                   tv.time_length,
                                   tv.context_path)
        query = query.filter(tv.timestamp.between(start_date, end_date))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def filter_by_period_of_time_and_course_id(self, start_date, end_date, course_id=()):
        tv = self.table
        query = self.session.query(tv.timestamp,
                                   tv.user_id,
                                   tv.session_id,
                                   tv.forum_id,
                                   tv.topic_id,
                                   tv.time_length,
                                   tv.context_path,
                                   tv.root_context_id.label('course_id'))
        query = query.filter(tv.timestamp.between(start_date, end_date)).filter(tv.root_context_id.in_(course_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def add_device_type(self, dataframe):
        new_df = add_device_type_(self.session, dataframe)
        return new_df

    def add_context_name(self, dataframe, course_id):
        new_df = add_context_name_(self.session, dataframe, course_id)
        return new_df

    def add_enrollment_type(self, dataframe, course_id):
        new_df = add_enrollment_type_(self.session, dataframe, course_id)
        return new_df


class QueryTopicFavorites(TableQueryMixin):

    table = TopicFavorites

    def filter_by_period_of_time(self, start_date, end_date):
        tf = self.table
        query = self.session.query(tf.timestamp,
                                   tf.session_id,
                                   tf.user_id,
                                   tf.topic_id,
                                   tf.creator_id,
                                   tf.root_context_id.label('course_id'))
        query = query.filter(tf.timestamp.between(start_date, end_date))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def filter_by_period_of_time_and_course_id(self, start_date, end_date, course_id=()):
        tf = self.table
        query = self.session.query(tf.timestamp,
                                   tf.session_id,
                                   tf.user_id,
                                   tf.topic_id,
                                   tf.creator_id,
                                   tf.root_context_id.label('course_id'))
        query = query.filter(tf.timestamp.between(start_date, end_date)).filter(tf.root_context_id.in_(course_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def add_device_type(self, dataframe):
        new_df = add_device_type_(self.session, dataframe)
        return new_df

    def add_context_name(self, dataframe, course_id):
        new_df = add_context_name_(self.session, dataframe, course_id)
        return new_df

    def add_enrollment_type(self, dataframe, course_id):
        new_df = add_enrollment_type_(self.session, dataframe, course_id)
        return new_df


class QueryTopicLikes(TableQueryMixin):

    table = TopicLikes

    def filter_by_period_of_time(self, start_date, end_date):
        tl = self.table
        query = self.session.query(tl.timestamp,
                                   tl.session_id,
                                   tl.user_id,
                                   tl.topic_id,
                                   tl.creator_id,
                                   tl.root_context_id.label('course_id'))
        query = query.filter(tl.timestamp.between(start_date, end_date))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def filter_by_period_of_time_and_course_id(self, start_date, end_date, course_id=()):
        tl = self.table
        query = self.session.query(tl.timestamp,
                                   tl.session_id,
                                   tl.user_id,
                                   tl.topic_id,
                                   tl.creator_id,
                                   tl.root_context_id.label('course_id'))
        query = query.filter(tl.timestamp.between(start_date, end_date)).filter(tl.root_context_id.in_(course_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def add_device_type(self, dataframe):
        new_df = add_device_type_(self.session, dataframe)
        return new_df

    def add_context_name(self, dataframe, course_id):
        new_df = add_context_name_(self.session, dataframe, course_id)
        return new_df

    def add_enrollment_type(self, dataframe, course_id):
        new_df = add_enrollment_type_(self.session, dataframe, course_id)
        return new_df
