#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics.database.enrollments import CourseDrops
from nti.analytics.database.enrollments import EnrollmentTypes
from nti.analytics.database.enrollments import CourseEnrollments
from nti.analytics.database.enrollments import CourseCatalogViews

from .mixins import TableQueryMixin

from . import orm_dataframe
from .common import add_device_type_

class QueryCourseCatalogViews(TableQueryMixin):

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

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		ccv = self.table
		query = self.session.query( ccv.timestamp,
									ccv.time_length,
									ccv.session_id,
									ccv.user_id,
									ccv.context_path).filter(ccv.timestamp.between(start_date, end_date)).filter(ccv.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

class QueryCourseEnrollments(TableQueryMixin):

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

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		ce = self.table
		query = self.session.query( ce.timestamp,
									ce.type_id,
									ce.session_id,
									ce.user_id).filter(ce.timestamp.between(start_date, end_date)).filter(ce.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

class QueryEnrollmentTypes(TableQueryMixin):
	table = EnrollmentTypes

	def get_enrollment_types(self):
		et = self.table
		query = self.session.query(et.type_id,
									et.type_name)
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryCourseDrops(TableQueryMixin):

	table = CourseDrops

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		cd = self.table
		query = self.session.query( cd.timestamp,
									cd.course_id,
									cd.session_id,
									cd.user_id).filter(cd.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		cd = self.table
		query = self.session.query( cd.timestamp,
									cd.course_id,
									cd.session_id,
									cd.user_id).filter(cd.timestamp.between(start_date, end_date)).filter(cd.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df
