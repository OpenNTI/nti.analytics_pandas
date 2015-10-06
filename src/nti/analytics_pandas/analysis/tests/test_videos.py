#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.videos import  VideoEventsTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestVideosEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestVideosEDA, self).setUp()

	def test_highlights_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(vet.dataframe.index), equal_to(1480))
		assert_that(vet.dataframe.columns, has_item('device_type'))

		event_by_date_df = vet.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(95))

		total_events = np.sum(event_by_date_df['total_video_events'])
		assert_that(total_events, equal_to(len(vet.dataframe.index)))

		unique_users_by_date = vet.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(95))

		ratio_df = vet.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(95))
