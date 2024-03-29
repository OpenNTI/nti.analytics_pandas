#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.queries.resource_views import QueryCourseResourceViews

from nti.analytics_pandas.tests import AnalyticsPandasTestBase


class TestResourceViews(AnalyticsPandasTestBase):

    def test_query_course_resources_views_by_period_of_time(self):
        start_date = u'2015-03-01'
        end_date = u'2015-05-31'
        qcrv = QueryCourseResourceViews(self.session)
        dataframe = qcrv.filter_by_period_of_time(start_date, end_date)
        assert_that(len(dataframe.index), equal_to(1))

    def test_query_course_resources_views_by_period_of_time_and_course_id(self):
        start_date = u'2015-01-01'
        end_date = u'2015-05-31'
        course_id = ['1024']
        qcrv = QueryCourseResourceViews(self.session)
        dataframe = qcrv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
        assert_that(len(dataframe.index), equal_to(1))

    def test_query_course_resource_views_add_resource_type(self):
        start_date = u'2015-01-01'
        end_date = u'2015-05-31'
        course_id = ['1024']
        qcrv = QueryCourseResourceViews(self.session)
        dataframe = qcrv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
        new_df = qcrv.add_resource_type(dataframe)
        assert_that(len(dataframe.index), equal_to(len(new_df.index)))
        assert_that(len(new_df), equal_to(1))
        assert_that(new_df.columns, has_item('resource_type'))

    def test_query_course_resource_views_add_device_type(self):
        start_date = u'2015-01-01'
        end_date = u'2015-05-31'
        course_id = ['1024']
        qcrv = QueryCourseResourceViews(self.session)
        dataframe = qcrv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
        new_df = qcrv.add_device_type(dataframe)
        assert_that(len(dataframe.index), equal_to(len(new_df.index)))
        assert_that(len(new_df), equal_to(1))
        assert_that(new_df.columns, has_item('device_type'))
