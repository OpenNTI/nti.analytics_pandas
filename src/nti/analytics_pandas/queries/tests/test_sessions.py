#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.queries.sessions import QuerySessions
from nti.analytics_pandas.queries.sessions import QueryUserAgents

from nti.analytics_pandas.tests import AnalyticsPandasTestBase


class TestSessions(AnalyticsPandasTestBase):

    def test_sessions(self):
        qs = QuerySessions(self.session)
        sessions_id = [0, 1, 2, 3, 4, 5]
        dataframe = qs.get_sessions_by_id(sessions_id)
        assert_that(len(dataframe.index), 5)
        assert_that(dataframe.columns, has_item('user_agent_id'))

    def test_user_agents(self):
        qua = QueryUserAgents(self.session)
        user_agents_id = [1]
        dataframe = qua.get_user_agents_by_id(user_agents_id)
        assert_that(len(dataframe.index), equal_to(1))
        assert_that(dataframe.columns, has_item('user_agent_id'))
        assert_that(dataframe.columns, has_item('user_agent'))

    def test_user_agents_device(self):
        qua = QueryUserAgents(self.session)
        user_agents_id = [1]

        dataframe = qua.get_user_agents_by_id(user_agents_id)
        new_df = qua.add_device_type(dataframe)
        assert_that(len(dataframe.index), equal_to(len(new_df.index)))

        index = dataframe[
			dataframe['user_agent_id'] == np.int(1)
		].index.tolist()
        assert_that(dataframe['device_type'].iloc[index[0]],
                    equal_to('Web App'))
