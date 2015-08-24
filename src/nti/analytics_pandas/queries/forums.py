#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.boards import ForumsCreated
from nti.analytics.database.boards import ForumCommentLikes
from nti.analytics.database.boards import ForumCommentsCreated
from nti.analytics.database.boards import ForumCommentFavorites

from nti.common.property import Lazy

from ..utils.orm_to_dataframe import orm_dataframe

class ForumsMixin(object):

	table = None

	def __init__(self, session):
		self.session = session

	@Lazy
	def columns(self):
		table = getattr(self.table, '__table__')
		return table.columns.keys()

class QueryForumsCreated(ForumsMixin):

	table = ForumsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		tc = self.table
		query = self.session.query(tc.timestamp,
								   tc.course_id,
								   tc.forum_ds_id,
								   tc.user_id,
								   tc.session_id).filter(tc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryForumsCommentsCreated(ForumsMixin):

	table = ForumCommentsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		fcc = self.table
		query = self.session.query(fcc.timestamp,
								   fcc.course_id,
								   fcc.user_id,
								   fcc.topic_id).filter(fcc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryForumCommentFavorites(ForumsMixin):

	table = ForumCommentFavorites

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		fcf = self.table
		query = self.session.query(fcf.timestamp,
								   fcf.session_id,
								   fcf.user_id,
								   fcf.comment_id,
								   fcf.creator_id,
								   fcf.course_id).filter(fcf.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryForumCommentLikes(ForumsMixin):

	table = ForumCommentLikes

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		fcl = ForumCommentLikes
		query = self.session.query(fcl.timestamp,
								   fcl.session_id,
								   fcl.user_id,
								   fcl.comment_id,
								   fcl.creator_id,
								   fcl.course_id).filter(fcl.timestamp.between(start_date, end_date))

		dataframe = orm_dataframe(query, self.columns)
		return dataframe
