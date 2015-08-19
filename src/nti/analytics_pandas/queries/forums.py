#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: forums.py 70252 2015-08-10 15:22:32Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"


from nti.analytics_pandas.utils.orm_to_dataframe import orm_dataframe
from nti.analytics.database.boards import ForumsCreated
from nti.analytics.database.boards import ForumCommentsCreated
from nti.analytics.database.boards import ForumCommentFavorites
from nti.analytics.database.boards import ForumCommentLikes

class QueryForumsCreated(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date = None, end_date = None):
		query = self.session.query(ForumsCreated.timestamp, ForumsCreated.course_id, ForumsCreated.forum_ds_id, ForumsCreated.user_id, ForumsCreated.session_id).filter(ForumsCreated.timestamp.between(start_date, end_date) )
		columns = ForumsCreated.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe
	

class QueryForumsCommentsCreated(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date=None, end_date = None):
		fcc = ForumCommentsCreated
		query = self.session.query(fcc.timestamp, fcc.course_id, fcc.user_id, fcc.topic_id).filter(fcc.timestamp.between(start_date, end_date))
		columns = ForumCommentsCreated.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe


class QueryForumCommentFavorites(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date=None, end_date = None):
		fcf = ForumCommentFavorites
		query = self.session.query(fcf.timestamp, fcf.session_id, fcf.user_id, fcf.comment_id, fcf.creator_id, fcf.course_id).filter(fcf.timestamp.between(start_date, end_date))
		columns = ForumCommentFavorites.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe

class QueryForumCommentLikes(object):
	def __init__(self, session):
		self.session = session

	def filter_by_period_of_time(self, start_date=None, end_date = None):
		fcl = ForumCommentLikes
		query = self.session.query(fcl.timestamp, fcl.session_id, fcl.user_id, fcl.comment_id, fcl.creator_id, fcl.course_id).filter(fcl.timestamp.between(start_date, end_date))
		columns = ForumCommentLikes.__table__.columns.keys()
		dataframe = orm_dataframe(query, columns)
		return dataframe



