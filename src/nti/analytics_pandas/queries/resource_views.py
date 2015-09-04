#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_views import CourseResourceViews

from nti.common.property import Lazy

from ..utils.orm_to_dataframe import orm_dataframe

class ResourceViewsMixin(object):

	table = None

	def __init__(self, session):
		self.session = session

	@Lazy
	def columns(self):
		table = getattr(self.table, '__table__')
		return table.columns.keys()

class QueryCourseResourceViews(ResourceViewsMixin):

	table = CourseResourceViews
	
	def filter_by_period_of_time(self, start_date=None, end_date=None):
		crv = self.table
		query = self.session.query( crv.resource_view_id,
									crv.timestamp,
									crv.course_id,
									crv.resource_id,
									crv.time_length,
									crv.session_id,
									crv.user_id,
									crv.context_path).filter(crv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
