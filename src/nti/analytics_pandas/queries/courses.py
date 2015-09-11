#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: courses.py 72785 2015-09-11 08:50:36Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics.database.root_context import Courses

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryCourses(TableQueryMixin):

	table = Courses

	def filter_by_context_name(self, context_name):
		c = self.table
		query = self.session.query(	c.context_id,
									c.context_ds_id,
									c.context_name,
									c.context_long_name,
									c.start_date,
									c.end_date,
									c.duration,
									c.term,
									c.crn).filter(c.context_name.like(context_name)).all()
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	