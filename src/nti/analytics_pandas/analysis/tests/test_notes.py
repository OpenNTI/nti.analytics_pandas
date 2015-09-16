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

from nti.analytics_pandas.analysis.notes import NotesViewTimeseries
from nti.analytics_pandas.analysis.notes import NoteLikesTimeseries
from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries
from nti.analytics_pandas.analysis.notes import NoteFavoritesTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase
from nti.analytics_pandas.utils import get_values_of_series_categorical_index_

class TestNotesEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestNotesEDA, self).setUp()

	def test_notes_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nct.dataframe.index), equal_to(34))
		assert_that(nct.dataframe.columns, has_item('device_type'))
		assert_that(nct.dataframe.columns, has_item('resource_type'))

		event_by_date_df = nct.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(20))

		total_events = np.sum(event_by_date_df['total_notes_created'])
		assert_that(total_events, equal_to(len(nct.dataframe.index)))

		unique_users_by_date = nct.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(20))

		ratio_df = nct.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(20))

		df = nct.analyze_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_note_created'))

		df = nct.analyze_resource_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_note_created'))

		df = nct.analyze_resource_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_note_created'))

	def test_notes_view_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nvt.dataframe.index), equal_to(157))
		assert_that(nvt.dataframe.columns, has_item('device_type'))
		assert_that(nvt.dataframe.columns, has_item('resource_type'))

		event_by_date_df = nvt.explore_number_of_events_based_timestamp_date()
		assert_that(len(event_by_date_df.index), equal_to(42))

		total_events = np.sum(event_by_date_df['total_notes_viewed'])
		assert_that(total_events, equal_to(len(nvt.dataframe.index)))

		unique_users_by_date = nvt.explore_unique_users_based_timestamp_date()
		assert_that(len(unique_users_by_date.index), equal_to(42))

		ratio_df = nvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(len(ratio_df.index), equal_to(42))

		df  = nvt.analyze_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_unique_notes_viewed'))

		most_viewed_notes = nvt.get_the_most_viewed_notes()
		assert_that(len(most_viewed_notes), equal_to(10))
		index_values = get_values_of_series_categorical_index_(most_viewed_notes)
		assert_that(type(index_values), equal_to(np.ndarray))

		most_viewed_notes_author_df = nvt.get_the_most_viewed_notes_and_its_author()
		assert_that(len(most_viewed_notes), len(most_viewed_notes_author_df))
		


	def test_note_likes_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nlt.dataframe.index), equal_to(0))

		event_by_date_df = nlt.explore_number_of_events_based_timestamp_date()
		assert_that(event_by_date_df, equal_to(None))

		unique_users_by_date = nlt.explore_unique_users_based_timestamp_date()
		assert_that(unique_users_by_date, equal_to(None))

		ratio_df = nlt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(ratio_df, equal_to(None))

	def test_note_favorites_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nft.dataframe.index), equal_to(0))

		event_by_date_df = nft.explore_number_of_events_based_timestamp_date()
		assert_that(event_by_date_df, equal_to(None))

		unique_users_by_date = nft.explore_unique_users_based_timestamp_date()
		assert_that(unique_users_by_date, equal_to(None))

		ratio_df = nft.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		assert_that(ratio_df, equal_to(None))

