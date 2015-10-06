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

from nti.analytics_pandas.analysis.topics import TopicViewsTimeseries
from nti.analytics_pandas.analysis.topics import TopicLikesTimeseries
from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries
from nti.analytics_pandas.analysis.topics import TopicFavoritesTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestTopicsEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicsEDA, self).setUp()

	def test_topics_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(tct.dataframe.index), equal_to(151))
		assert_that(tct.dataframe.columns, has_item('device_type'))

		event_by_date_df = tct.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(2))

		total_events = np.sum(event_by_date_df['total_topics_created'])
		assert_that(total_events, equal_to(len(tct.dataframe.index)))

		unique_users_by_date = tct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(2))

		ratio_df = tct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(2))

	def test_topic_views_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(tvt.dataframe.index), equal_to(1610))
		assert_that(tvt.dataframe.columns, has_item('device_type'))

		event_by_date_df = tvt.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(109))

		total_events = np.sum(event_by_date_df['total_topics_viewed'])
		assert_that(total_events, equal_to(len(tvt.dataframe.index)))

		unique_users_by_date = tvt.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(109))

		ratio_df = tvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(109))

	def test_topic_likes_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(tlt.dataframe.index), equal_to(0))

		event_by_date_df = tlt.explore_number_of_events_based_timestamp_date()
		assert_that(event_by_date_df, equal_to(None))

		unique_users_by_date = tlt.explore_unique_users_based_timestamp_date()
		assert_that(unique_users_by_date, equal_to(None))

		ratio_df = tlt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(ratio_df, equal_to(None))

	def test_topic_favorites_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(tft.dataframe.index), equal_to(6))
		assert_that(tft.dataframe.columns, has_item('device_type'))

		event_by_date_df = tft.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(4))

		total_events = np.sum(event_by_date_df['total_topic_favorites'])
		assert_that(total_events, equal_to(len(tft.dataframe.index)))

		unique_users_by_date = tft.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(4))

		ratio_df = tft.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(4))
