#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.queries.courses import QueryCourses

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourses(AnalyticsPandasTestBase):

	def test_filter_by_context_name(self):
		qc = QueryCourses(self.session)
		context_name = u'name'
		dataframe = qc.filter_by_context_name(context_name)
		assert_that(len(dataframe.index), equal_to(6))

		context_name = u'another_name'
		dataframe = qc.filter_by_context_name(context_name)
		assert_that(len(dataframe.index), equal_to(1))

	def test_filter_by_context_ids(self):
		qc = QueryCourses(self.session)
		context_ids = ['1024']
		dataframe = qc.filter_by_context_ids(context_ids)
		assert_that(len(dataframe.index), equal_to(1))

	def test_get_context_name(self):
		qc = QueryCourses(self.session)
		context_ids = ['1024']
		dataframe = qc.get_context_name(context_ids)
		assert_that(len(dataframe.index), equal_to(1))

	def test_get_course_id(self):
		qc = QueryCourses(self.session)
		context_name = 'name'
		dataframe = qc.get_course_id(context_name)
		assert_that(len(dataframe.index), equal_to(6))
		course_ids = dataframe['context_id'].tolist()
		assert_that(course_ids, has_item(1024))
		assert_that(course_ids, has_item(1025))
		assert_that(course_ids, has_item(1026))
		assert_that(course_ids, has_item(1027))
		assert_that(course_ids, has_item(1028))
		assert_that(course_ids, has_item(1029))

		dataframe = qc.get_course_id(context_name, start_date='2015-01-01', end_date='2015-05-31')
		assert_that(course_ids, has_item(1024))
		assert_that(course_ids, has_item(1025))
		assert_that(course_ids, has_item(1026))
		assert_that(course_ids, has_item(1027))
		assert_that(course_ids, has_item(1028))
		assert_that(course_ids, has_item(1029))

	def test_get_course_given_ntiid(self):
		qc = QueryCourses(self.session)
		context_ds_id = u'ds'
		dataframe = qc.get_course_given_ntiid(context_ds_id)
		assert_that(len(dataframe.index), equal_to(7))
		course_ids = dataframe['context_id'].tolist()
		assert_that(course_ids, has_item(1024))
		assert_that(course_ids, has_item(1025))
		assert_that(course_ids, has_item(1026))
		assert_that(course_ids, has_item(1027))
		assert_that(course_ids, has_item(1028))
		assert_that(course_ids, has_item(1029))
		assert_that(course_ids, has_item(1030))

