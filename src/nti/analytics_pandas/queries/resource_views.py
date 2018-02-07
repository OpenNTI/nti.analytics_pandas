#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.analytics_database.resource_views import CourseResourceViews

from nti.analytics_pandas.queries.common import add_device_type_
from nti.analytics_pandas.queries.common import add_context_name_
from nti.analytics_pandas.queries.common import add_resource_type_

from nti.analytics_pandas.queries.enrollments import add_enrollment_type_

from nti.analytics_pandas.queries.mixins import TableQueryMixin

from nti.analytics_pandas.utils.dataframe_operation import orm_dataframe

logger = __import__('logging').getLogger(__name__)


class QueryCourseResourceViews(TableQueryMixin):

    table = CourseResourceViews

    def filter_by_period_of_time(self, start_date=None, end_date=None):
        crv = self.table
        query = self.session.query(crv.resource_view_id,
                                   crv.timestamp,
                                   crv.root_context_id.label('course_id'),
                                   crv.resource_id,
                                   crv.time_length,
                                   crv.session_id,
                                   crv.user_id,
                                   crv.context_path).filter(crv.timestamp.between(start_date, end_date))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
        crv = self.table
        query = self.session.query(crv.resource_view_id,
                                   crv.timestamp,
                                   crv.resource_id,
                                   crv.time_length,
                                   crv.session_id,
                                   crv.user_id,
                                   crv.context_path,
                                   crv.root_context_id.label('course_id'))
        query = query.filter(crv.timestamp.between(start_date, end_date)).filter(crv.root_context_id.in_(course_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def add_resource_type(self, dataframe):
        new_df = add_resource_type_(self.session, dataframe)
        return new_df

    def add_device_type(self, dataframe):
        new_df = add_device_type_(self.session, dataframe)
        return new_df

    def add_context_name(self, dataframe, course_id):
        new_df = add_context_name_(self.session, dataframe, course_id)
        return new_df

    def add_enrollment_type(self, dataframe, course_id):
        new_df = add_enrollment_type_(self.session, dataframe, course_id)
        return new_df
