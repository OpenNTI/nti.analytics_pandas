#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that
from hamcrest import has_item

import numpy as np

from nti.analytics_pandas.analysis.enrollments import CourseCatalogViewsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseEnrollmentsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseDropsTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourseCatalogViewsEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestCourseCatalogViewsEDA, self).setUp()

	def test_course_catalog_views_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(ccvt.dataframe.columns, has_item('device_type'))
		events_df = ccvt.explore_number_of_events_based_timestamp_date()
		assert_that(len(events_df.index), equal_to(109))
		total_events = np.sum(events_df['total_course_catalog_views'])
		assert_that(total_events, equal_to(409))


		unique_users_df = ccvt.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_df.index), equal_to(109))
		ratio_df = ccvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(109))

		df = ccvt.analyze_device_types()
		assert_that(len(df.index), equal_to(133))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('average_time_length'))
		assert_that(len(df.sum(level = 'timestamp_period')), equal_to(109))

	def test_course_enrollments_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(cet.dataframe.columns, has_item('device_type'))
		events_df = cet.explore_number_of_events_based_timestamp_date()
		assert_that(len(events_df.index), equal_to(100))
		total_events = np.sum(events_df['total_enrollments'])
		assert_that(total_events, equal_to(571))

		unique_users_df = cet.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_df.index), equal_to(100))

		ratio_df = cet.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(100))
	
		df = cet.analyze_device_enrollment_types()
		#the length of df.sum(level = 'timestamp_period') should be equal to the length of ratio_df,
		#yet some session_id values are null
		assert_that(len(df.sum(level = 'timestamp_period')), equal_to(93))


	def test_course_drops_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(cdt.dataframe.columns, has_item('device_type'))
		events_df = cdt.explore_number_of_events_based_timestamp_date()
		assert_that(len(events_df.index), equal_to(19))
		total_events = np.sum(events_df['total_drops'])
		assert_that(total_events, equal_to(23))


		unique_users_df = cdt.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_df.index), equal_to(19))

		ratio_df = cdt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(19))


