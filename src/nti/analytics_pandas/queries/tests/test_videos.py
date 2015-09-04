#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.queries.videos import QueryVideoEvents

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestVideos(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestVideos, self).setUp()

	def test_query_video_events_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qve = QueryVideoEvents(self.session)
		dataframe = qve.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(105505))