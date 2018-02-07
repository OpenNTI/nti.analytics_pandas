#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.analytics_database.users import Users

from nti.analytics_pandas.queries.mixins import TableQueryMixin

from nti.analytics_pandas.utils.dataframe_operation import orm_dataframe

logger = __import__('logging').getLogger(__name__)


class QueryUsers(TableQueryMixin):

    table = Users

    def filter_by_user_id(self, users_id):
        u = self.table
        query = self.session.query(u.user_id,
                                   u.user_ds_id,
                                   u.username,
                                   u.username2,
                                   u.allow_research,
                                   u.create_date).filter(u.user_id.in_(users_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def get_username_filter_by_user_id(self, users_id):
        u = self.table
        query = self.session.query(u.user_id,
                                   u.username).filter(u.user_id.in_(users_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe
