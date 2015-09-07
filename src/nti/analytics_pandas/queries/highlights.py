#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_tags import HighlightsCreated

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryHighlightsCreated(TableQueryMixin):

	table = HighlightsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		hc = self.table
		query = self.session.query( hc.highlight_id,
									hc.timestamp,
									hc.deleted,
									hc.resource_id,
									hc.session_id,
									hc.user_id,
									hc.course_id).filter(hc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		hc = self.table
		query = self.session.query( hc.highlight_id,
									hc.timestamp,
									hc.deleted,
									hc.resource_id,
									hc.session_id,
									hc.user_id).filter(hc.timestamp.between(start_date, end_date)).filter(hc.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
