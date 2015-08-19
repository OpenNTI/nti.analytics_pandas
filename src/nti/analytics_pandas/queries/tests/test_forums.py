#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: test_forums.py 70252 2015-08-10 15:22:32Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"


from hamcrest import is_
from hamcrest import none
from hamcrest import equal_to
from hamcrest import not_none
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than
from hamcrest import less_than_or_equal_to

from nti.analytics_pandas.tests import AnalyticsPandasTestBase
from nti.analytics_pandas.queries.forums import QueryForumsCreated
from nti.analytics_pandas.queries.forums import QueryForumsCommentsCreated
from nti.analytics_pandas.queries.forums import QueryForumCommentFavorites
from nti.analytics_pandas.queries.forums import QueryForumCommentLikes

class TestForums(AnalyticsPandasTestBase):
	def setUp(self):
		super(TestForums, self).setUp()

	def test_query_forums_created_by_period_of_time(self):
		start_date = u'2015-03-01' 
		end_date = u'2015-05-31'
		qfc = QueryForumsCreated(self.session)
		dataframe = qfc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(34))

	def test_query_forums_comments_created_by_period_of_time(self):
		start_date = u'2015-03-01' 
		end_date = u'2015-05-31'
		qfcc = QueryForumsCommentsCreated(self.session)
		dataframe = qfcc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(3164))

	def test_query_forums_comment_favorites_by_period_of_time(self):
		start_date = u'2015-03-01' 
		end_date = u'2015-05-31'
		qfcf = QueryForumCommentFavorites(self.session)
		dataframe = qfcf.filter_by_period_of_time(start_date,end_date)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_forums_comment_likes_by_period_of_time(self):
		start_date = u'2015-03-01' 
		end_date = u'2015-05-31'
		qfcl = QueryForumCommentLikes(self.session)
		dataframe = qfcl.filter_by_period_of_time(start_date,end_date)
		assert_that(len(dataframe.index), equal_to(78))
