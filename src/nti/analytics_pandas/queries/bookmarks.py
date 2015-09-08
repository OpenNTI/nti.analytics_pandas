#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_tags import BookmarksCreated

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryBookmarksCreated(TableQueryMixin):

	table = BookmarksCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		bc = self.table
		query = self.session.query( bc.bookmark_id,
									bc.timestamp,
									bc.deleted,
									bc.resource_id,
									bc.session_id,
									bc.user_id,
									bc.course_id).filter(bc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		print(course_id)
		bc = self.table
		query = self.session.query( bc.bookmark_id,
									bc.timestamp,
									bc.deleted,
									bc.resource_id,
									bc.session_id,
									bc.user_id).filter(bc.timestamp.between(start_date, end_date)).filter(bc.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
