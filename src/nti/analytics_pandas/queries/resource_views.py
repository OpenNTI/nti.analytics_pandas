#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_views import CourseResourceViews

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryCourseResourceViews(TableQueryMixin):

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

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=[]):
		crv = self.table
		query = self.session.query( crv.resource_view_id,
									crv.timestamp,
									crv.resource_id,
									crv.time_length,
									crv.session_id,
									crv.user_id,
									crv.context_path).filter(crv.timestamp.between(start_date, end_date)).filter(crv.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
