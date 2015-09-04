#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: highlights.py 71540 2015-08-24 16:41:40Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_tags import HighlightsCreated

from nti.common.property import Lazy

from ..utils.orm_to_dataframe import orm_dataframe

class HighlightsMixin(object):

	table = None

	def __init__(self, session):
		self.session = session

	@Lazy
	def columns(self):
		table = getattr(self.table, '__table__')
		return table.columns.keys()

class QueryHighlightsCreated(HighlightsMixin):

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
