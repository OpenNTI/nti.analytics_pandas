#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.forums import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCommentsCreatedTimeseries
from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestForumsCreatedEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestForumsCreatedEDA, self).setUp()

	def test_forums_created_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)

		events_df = fct.explore_number_of_events_based_timestamp_date()
		assert_that(len(events_df.index), equal_to(1))
		total_events = np.sum(events_df['total_forums_created'])
		assert_that(total_events, equal_to(4))


		unique_users_df = fct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_df.index), equal_to(1))

		ratio_df = fct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(1))

	def test_forums_comments_created_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)

		events_df = fcct.explore_number_of_events_based_timestamp_date()
		assert_that(len(events_df.index), equal_to(70))
		total_events = np.sum(events_df['total_forums_comments_created'])
		assert_that(total_events, equal_to(205))

		unique_users_df = fcct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_df.index), equal_to(70))

		ratio_df = fcct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(70))