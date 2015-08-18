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
from zope import component

from nti.analytics.database.interfaces import IAnalyticsDB
from nti.analytics.database.database import AnalyticsDB
from nti.analytics.database.sessions import get_session_by_id
from nti.analytics.database.sessions import Sessions


class TestConnection(unittest.TestCase):
	def setUp(self):
		self.db = AnalyticsDB( dburi="mysql+pymysql://root@localhost:3306/Analytics")
		component.getGlobalSiteManager().registerUtility( self.db, IAnalyticsDB )
		self.session = self.db.session

	def tearDown(self):
		component.getGlobalSiteManager().unregisterUtility( self.db )
		self.session.close()
	
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
		
		
