#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.exploratory_data_analysis.bookmarks_eda import BookmarkCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestBookmarksEDA(AnalyticsPandasTestBase):
	def setUp(self):
		super(TestBookmarksEDA, self).setUp()

	def test_explore_number_of_events_based_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(bct.dataframe.index), equal_to(54))
		
		event_by_date_df = bct.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(20))

		unique_users_by_date = bct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(20))

		ratio_df = bct.explore_ratio_of_events_over_unique_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(20))