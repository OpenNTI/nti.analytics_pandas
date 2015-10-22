#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: assessments.py 73525 2015-09-23 19:15:51Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.assessments import AssignmentViews
from nti.analytics_database.assessments import AssignmentsTaken
from nti.analytics_database.assessments import SelfAssessmentViews
from nti.analytics_database.assessments import SelfAssessmentsTaken 

from .mixins import TableQueryMixin

from .common import add_device_type_
from .common import add_resource_type_

from . import orm_dataframe

class QueryAssignmentViews(TableQueryMixin):

	table = AssignmentViews

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		av = self.table
		query = self.session.query(	av.timestamp,
									av.context_path,
									av.time_length,
									av.assignment_view_id,
									av.resource_id,
									av.session_id,
									av.user_id,
									av.assignment_id,
									av.entity_root_context_id).filter(av.timestamp.between(start_date, end_date)).filter(av.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_resource_type(self, dataframe):
		new_df = add_resource_type_(self.session, dataframe)
		return new_df

class QueryAssignmentsTaken(TableQueryMixin):

	table = AssignmentsTaken

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		at = self.table
		query = self.session.query(	at.timestamp,
									at.time_length,
									at.submission_id,
									at.assignment_taken_id,
									at.assignment_id,
									at.session_id,
									at.user_id,
									at.is_late).filter(at.timestamp.between(start_date, end_date)).filter(at.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

class QuerySelfAssessmentViews(TableQueryMixin):

	table = SelfAssessmentViews

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		sav = self.table
		query = self.session.query(	sav.timestamp,
									sav.context_path,
									sav.time_length,
									sav.self_assessment_view_id,
									sav.resource_id,
									sav.session_id,
									sav.user_id,
									sav.assignment_id,
									sav.entity_root_context_id).filter(sav.timestamp.between(start_date, end_date)).filter(sav.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_resource_type(self, dataframe):
		new_df = add_resource_type_(self.session, dataframe)

class QuerySelfAssessmentsTaken(TableQueryMixin):

	table = SelfAssessmentsTaken

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		sat = self.table
		query = self.session.query(	sat.timestamp,
									sat.time_length,
									sat.submission_id,
									sat.self_assessment_id,
									sat.assignment_id,
									sat.session_id,
									sat.user_id).filter(sat.timestamp.between(start_date, end_date)).filter(sat.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df