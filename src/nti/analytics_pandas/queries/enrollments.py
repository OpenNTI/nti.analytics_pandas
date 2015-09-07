#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.enrollments import CourseDrops
from nti.analytics.database.enrollments import EnrollmentTypes
from nti.analytics.database.enrollments import CourseEnrollments
from nti.analytics.database.enrollments import CourseCatalogViews

from nti.common.property import Lazy

from . import orm_dataframe

class EnrollmentsMixin(object):

	table = None

	def __init__(self, session):
		self.session = session

	@Lazy
	def columns(self):
		table = getattr(self.table, '__table__')
		return table.columns.keys()

class QueryCourseCatalogViews(EnrollmentsMixin):

	table = CourseCatalogViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ccv = self.table
		query = self.session.query( ccv.timestamp,
									ccv.course_id,
									ccv.time_length,
									ccv.session_id,
									ccv.user_id,
									ccv.context_path).filter(ccv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryCourseEnrollments(EnrollmentsMixin):

	table = CourseEnrollments

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ce = self.table
		query = self.session.query( ce.timestamp,
									ce.course_id,
									ce.type_id,
									ce.session_id,
									ce.user_id).filter(ce.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryEnrollmentTypes(EnrollmentsMixin):

	table = EnrollmentTypes

	def get_enrollment_types(self):
		et = self.table
		query = self.session.query(et.type_id,
									et.type_name)
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryCourseDrops(EnrollmentsMixin):

	table = CourseDrops

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		cd = self.table
		query = self.session.query( cd.timestamp,
									cd.course_id,
									cd.session_id,
									cd.user_id).filter(cd.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
