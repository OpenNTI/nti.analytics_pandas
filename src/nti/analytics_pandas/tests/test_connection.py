#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=no-member

from hamcrest import equal_to
from hamcrest import assert_that
from hamcrest import greater_than

from sqlalchemy.orm.session import make_transient

from nti.analytics_database.sessions import Sessions

from nti.analytics_pandas.utils.orm_to_dataframe import orm_dataframe

from nti.analytics_pandas.tests import AnalyticsPandasTestBase


def get_session_by_id(session, session_id):
    query = session.query(Sessions)
    session_record = query.filter(Sessions.session_id == session_id).first()
    if session_record:
        make_transient(session_record)
    return session_record


class TestConnection(AnalyticsPandasTestBase):

    def test_query_get_session_by_id(self):
        result = get_session_by_id(self.session, 2)
        assert_that(result.user_id, equal_to(1))

    def test_query_count_session(self):
        result = self.session.query(Sessions).count()
        assert_that(result, greater_than(0))

    def test_query_session(self):
        query = self.session.query(Sessions).limit(10)
        columns = getattr(Sessions, '__table__').columns.keys()
        assert_that(len(columns), equal_to(6))
        orm_dataframe(query, columns)
