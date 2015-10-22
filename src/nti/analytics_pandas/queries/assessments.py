#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: assessments.py 73525 2015-09-23 19:15:51Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.assessments import AssignmentViews

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