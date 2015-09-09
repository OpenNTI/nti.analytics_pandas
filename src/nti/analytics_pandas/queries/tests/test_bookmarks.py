#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.queries.bookmarks import QueryBookmarksCreated

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestBookmarks(AnalyticsPandasTestBase):
	def setUp(self):
		super(TestBookmarks, self).setUp()

	def test_query_bookmarks_created_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qbc = QueryBookmarksCreated(self.session)
		dataframe = qbc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(160))

	def test_query_bookmarks_created_by_time_period_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qbc = QueryBookmarksCreated(self.session)
		dataframe = qbc.filter_by_course_id_and_period_of_time(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(54))