#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.resource_views import VideoEvents

from nti.analytics_pandas.queries.common import add_device_type_
from nti.analytics_pandas.queries.common import add_context_name_
from nti.analytics_pandas.queries.common import add_resource_type_

from nti.analytics_pandas.queries.mixins import TableQueryMixin

from nti.analytics_pandas.queries.enrollments import add_enrollment_type_

from nti.analytics_pandas.utils.dataframe_operation import orm_dataframe


class QueryVideoEvents(TableQueryMixin):

    table = VideoEvents

    def filter_by_period_of_time(self, start_date=None, end_date=None):
        ve = self.table
        query = self.session.query(ve.video_view_id,
                                   ve.timestamp,
                                   ve.root_context_id.label('course_id'),
                                   ve.resource_id,
                                   ve.context_path,
                                   ve.time_length,
                                   ve.video_event_type,
                                   ve.video_start_time,
                                   ve.video_end_time,
                                   ve.with_transcript,
                                   ve.session_id,
                                   ve.user_id,
                                   ve.play_speed)
        query = query.filter(ve.timestamp.between(start_date, end_date))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
        ve = self.table
        query = self.session.query(ve.video_view_id,
                                   ve.timestamp,
                                   ve.resource_id,
                                   ve.context_path,
                                   ve.time_length,
                                   ve.video_event_type,
                                   ve.video_start_time,
                                   ve.video_end_time,
                                   ve.with_transcript,
                                   ve.session_id,
                                   ve.user_id,
                                   ve.play_speed,
                                   ve.root_context_id.label('course_id'))
        query = query.filter(ve.timestamp.between(start_date, end_date))
        query = query.filter(ve.root_context_id.in_(course_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def add_device_type(self, dataframe):
        new_df = add_device_type_(self.session, dataframe)
        return new_df

    def add_resource_type(self, dataframe):
        new_df = add_resource_type_(self.session, dataframe)
        return new_df

    def add_context_name(self, dataframe, course_id):
        new_df = add_context_name_(self.session, dataframe, course_id)
        return new_df

    def add_enrollment_type(self, dataframe, course_id):
        new_df = add_enrollment_type_(self.session, dataframe, course_id)
        return new_df
