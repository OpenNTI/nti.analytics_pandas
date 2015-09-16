#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: users.py 72803 2015-09-11 15:50:12Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics.database.users import Users

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryUsers(TableQueryMixin):

	table = Users

	def filter_by_user_id(self, users_id):
		u = self.table
		query = self.session.query(	u.user_id,
									u.user_ds_id,
									u.username,
									u.username2,
									u.allow_research,
									u.create_date).filter(u.user_id.in_(users_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
