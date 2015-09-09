#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

import numpy as np

class TestTopicsEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicsEDA, self).setUp()

	def test_topics_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(tct.dataframe.index), equal_to(151))

		event_by_date_df = tct.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(2))

		total_events = np.sum(event_by_date_df['total_topics_created'])
		assert_that(total_events, equal_to(len(tct.dataframe.index)))

		unique_users_by_date = tct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(2))

		ratio_df = tct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(2))
