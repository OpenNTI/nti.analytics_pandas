#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

import numpy as np

class TestNotesEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestNotesEDA, self).setUp()

	def test_highlights_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nct.dataframe.index), equal_to(34))

		event_by_date_df = nct.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(20))

		total_events = np.sum(event_by_date_df['total_notes_created'])
		assert_that(total_events, equal_to(len(nct.dataframe.index)))

		unique_users_by_date = nct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(20))

		ratio_df = nct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(20))
