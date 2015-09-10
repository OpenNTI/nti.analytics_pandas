#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics.database.sessions import Sessions
from nti.analytics.database.sessions import UserAgents

from .mixins import TableQueryMixin

from . import orm_dataframe

class QuerySessions(TableQueryMixin):

	table = Sessions

	def get_sessions_by_id(self, sessions_id):
		s = self.table
		query = self.session.query(	s.session_id,
									s.user_id,
									s.ip_addr,
									s.user_agent_id,
									s.start_time,
									s.end_time).filter(s.session_id.in_(sessions_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe


class QueryUserAgents(TableQueryMixin):

	table = UserAgents

	def get_user_agents_by_id(self, user_agents_id):
		ua = self.table
		query = self.session.query(	ua.user_agent_id,
									ua.user_agent).filter(ua.user_agent_id.in_(user_agents_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
