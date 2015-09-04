#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.queries.resource_views import QueryCourseResourceViews

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViews(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestResourceViews, self).setUp()

	def test_query_course_catalog_views_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qcrv = QueryCourseResourceViews(self.session)
		dataframe = qcrv.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(76756))