#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from nti.analytics_pandas.queries.users import QueryUsers

from nti.analytics_pandas.tests import AnalyticsPandasTestBase


class TestCourses(AnalyticsPandasTestBase):

    def test_filter_by_user_id(self):
        qu = QueryUsers(self.session)
        users_id = [1, 2, 3, 4, 5]
        qu.filter_by_user_id(users_id)
