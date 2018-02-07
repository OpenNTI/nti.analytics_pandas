#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import equal_to
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.queries.resources import QueryResources

from nti.analytics_pandas.tests import AnalyticsPandasTestBase


class TestResources(AnalyticsPandasTestBase):

    def test_get_all_resources(self):
        qr = QueryResources(self.session)
        dataframe = qr.get_all_resources()
        assert_that(dataframe['resource_display_name'].iloc[0], 
					equal_to('video'))

    def test_get_resources_ds_id_given_id(self):
        qr = QueryResources(self.session)
        resources_id = (1,)
        dataframe = qr.get_resources_ds_id_given_id(resources_id)
        assert_that(len(dataframe.index), equal_to(1))
        assert_that(dataframe.resource_id.iloc[0], equal_to(1))

    def test_get_resources_given_id(self):
        qr = QueryResources(self.session)
        resources_id = (1,)
        dataframe = qr.get_resources_given_id(resources_id)
        assert_that(len(dataframe.index), equal_to(1))
        assert_that(dataframe.resource_id.iloc[0], equal_to(1))
        assert_that(dataframe['max_time_length'].iloc[0], equal_to(500))

    def test_add_resource_type(self):
        qr = QueryResources(self.session)
        dataframe = qr.get_all_resources()
        dataframe = qr.add_resource_type(dataframe)
        assert_that(dataframe['resource_type'].iloc[0], equal_to(u'video'))

        index = dataframe[dataframe['resource_id'] == np.int(1)].index.tolist()
        idx = index[0]
        assert_that(dataframe['resource_type'].iloc[idx], equal_to(u'video'))
