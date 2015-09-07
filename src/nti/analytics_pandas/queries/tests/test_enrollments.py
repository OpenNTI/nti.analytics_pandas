#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.queries.enrollments import QueryCourseDrops
from nti.analytics_pandas.queries.enrollments import QueryEnrollmentTypes
from nti.analytics_pandas.queries.enrollments import QueryCourseEnrollments
from nti.analytics_pandas.queries.enrollments import QueryCourseCatalogViews

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestEnrollments(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestEnrollments, self).setUp()

	def test_query_course_catalog_views_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qccv = QueryCourseCatalogViews(self.session)
		dataframe = qccv.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(4880))

	def test_query_course_catalog_views_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qccv = QueryCourseCatalogViews(self.session)
		dataframe = qccv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(409))

	def test_query_course_enrollments_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qce = QueryCourseEnrollments(self.session)
		dataframe = qce.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(2718))

	def test_query_course_enrollments_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qce = QueryCourseEnrollments(self.session)
		dataframe = qce.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(571))

	def test_query_course_drops_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qcd = QueryCourseDrops(self.session)
		dataframe = qcd.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(180))

	def test_query_course_drops_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qcd = QueryCourseDrops(self.session)
		dataframe = qcd.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(23))

	def test_query_enrollment_types(self):
		qet = QueryEnrollmentTypes(self.session)
		dataframe = qet.get_enrollment_types()
		assert_that(len(dataframe.index), equal_to(5))

