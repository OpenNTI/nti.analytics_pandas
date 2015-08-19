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
		

