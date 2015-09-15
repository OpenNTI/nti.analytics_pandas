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

from nti.analytics_pandas.analysis.highlights import HighlightsCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestHighlightsEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestHighlightsEDA, self).setUp()

	def test_highlights_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(hct.dataframe.index), equal_to(779))
		assert_that(hct.dataframe.columns, has_item('device_type'))
		assert_that(hct.dataframe.columns, has_item('resource_type'))

		event_by_date_df = hct.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(36))

		total_events = np.sum(event_by_date_df['total_highlights_created'])
		assert_that(total_events, equal_to(len(hct.dataframe.index)))

		unique_users_by_date = hct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(36))

		ratio_df = hct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(36))

		df = hct.analyze_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_highlight_created'))
