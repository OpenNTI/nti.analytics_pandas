#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from hamcrest import is_
from hamcrest import none
from hamcrest import equal_to
from hamcrest import not_none
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than
from hamcrest import less_than_or_equal_to

import zope.testing.cleanup

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

from nti.analytics.database.sessions import get_session_by_id
from nti.analytics.database.sessions import Sessions
from nti.analytics.database.boards import ForumsCreated

from nti.analytics_pandas.utils.orm_to_dataframe import orm_dataframe

from nti.analytics_pandas.queries.forums import QueryForumsCreated

class TestConnection(AnalyticsPandasTestBase):
	def setUp(self):
		super( TestConnection, self ).setUp()

	def test_query_get_session_by_id(self):
		result = get_session_by_id(1)
		assert_that (result.user_id, equal_to(184))

	def test_query_count_session(self):
		result = self.session.query( Sessions ).count()
		assert_that(result, greater_than(100000))

	def test_query_session(self):
		query = self.session.query(Sessions).limit(10)
		columns = Sessions.__table__.columns.keys()
		assert_that(len(columns), equal_to(6))
		result = orm_dataframe(query, columns)