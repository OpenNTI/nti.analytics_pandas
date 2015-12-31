#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: social.py 78654 2015-12-09 17:07:38Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.social import ContactsAdded
from nti.analytics_database.social import ContactsRemoved

from nti.analytics_database.social import DynamicFriendsListsCreated
from nti.analytics_database.social import DynamicFriendsListsMemberAdded
from nti.analytics_database.social import DynamicFriendsListsMemberRemoved

from nti.analytics_database.social import FriendsListsCreated
from nti.analytics_database.social import FriendsListsMemberAdded
from nti.analytics_database.social import FriendsListsMemberRemoved

from .mixins import TableQueryMixin

from .common import add_application_type_

from . import orm_dataframe


class QueryDynamicFriendsListsCreated(TableQueryMixin):

	table = DynamicFriendsListsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		dflc = self.table
		query = self.session.query(dflc.timestamp,
								   dflc.deleted,
								   dflc.dfl_ds_id,
								   dflc.dfl_id,
								   dflc.session_id,
								   dflc.user_id).filter(dflc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryDynamicFriendsListsMemberAdded(TableQueryMixin):

	table = DynamicFriendsListsMemberAdded

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		dflma = self.table
		query = self.session.query(dflma.timestamp,
								   dflma.session_id,
								   dflma.user_id,
								   dflma.dfl_id,
								   dflma.target_id
								   ).filter(dflma.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryDynamicFriendsListsMemberRemoved(TableQueryMixin):

	table = DynamicFriendsListsMemberRemoved

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		dflmr = self.table
		query = self.session.query(dflmr.timestamp,
								   dflmr.session_id,
								   dflmr.user_id,
								   dflmr.dfl_id,
								   dflmr.target_id
								   ).filter(dflmr.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df