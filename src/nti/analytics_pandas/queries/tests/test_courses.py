#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.queries.courses import QueryCourses

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourses(AnalyticsPandasTestBase):
	def setUp(self):
		super(TestCourses, self).setUp()

	def test_filter_by_context_name(self):
		qc = QueryCourses(self.session)
		context_name = u'%ANTH%'
		dataframe = qc.filter_by_context_name(context_name)
		assert_that(len(dataframe.index), equal_to(6))

		context_name = u'%ANTH%1613%'
		dataframe = qc.filter_by_context_name(context_name)
		assert_that(len(dataframe.index), equal_to(3))

	def test_filter_by_context_ids(self):
		qc = QueryCourses(self.session)
		context_ids = ['1068', '1096', '1097', '1098', '1099']
		dataframe = qc.filter_by_context_ids(context_ids)
		assert_that(len(dataframe.index), equal_to(5))

	def test_get_context_name(self):
		qc = QueryCourses(self.session)
		context_ids = ['1068', '1096', '1097', '1098', '1099']
		dataframe = qc.get_context_name(context_ids)
		assert_that(len(dataframe.index), equal_to(5))
