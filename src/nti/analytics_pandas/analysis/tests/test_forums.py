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

from nti.analytics_pandas.analysis.forums import ForumsEventsTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentLikesTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCommentsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentFavoritesTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestForumsCreatedEDA(AnalyticsPandasTestBase):

	def test_forums_comments_created_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['1024']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		assert_that(fcct.dataframe.columns, has_item('context_name'))

		events_df = fcct.analyze_events()
		assert_that(len(events_df.index), equal_to(1))
		total_events = np.sum(events_df['number_of_comment_created'])
		assert_that(total_events, equal_to(len(fcct.dataframe.index)))

		df = fcct.analyze_device_types()
		assert_that(df.columns, has_item('number_of_comment_created'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('average_comment_length'))
		assert_that(df.columns, has_item('favorite_count'))
		assert_that(df.columns, has_item('like_count'))
		total_events = np.sum(df['number_of_comment_created'])

		most_active_users_df = fcct.get_the_most_active_users(max_rank_number=10)
		assert_that(len(most_active_users_df.index), equal_to(1))

		df = fcct.analyze_comments_per_section()
		assert_that(df.columns, has_item('number_of_comment_created'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_forums_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['1024']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fet = ForumsEventsTimeseries(fct, fcct, fclt, fcft)

		df = fet.combine_all_events_per_date()
		assert_that(len(df.index), equal_to(3))
		assert_that(len(df.columns), equal_to(5))
