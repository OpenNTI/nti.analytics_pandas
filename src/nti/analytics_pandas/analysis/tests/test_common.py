#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.common import get_data

from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCommonFunctions(AnalyticsPandasTestBase):

	def test_get_data(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1024']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(tct.dataframe.columns, has_item('device_type'))
		assert_that(tct.dataframe.columns, has_item('context_name'))
		assert_that(tct.dataframe.columns, has_item('enrollment_type'))

		data = get_data(tct)
		assert_that(data['df_by_timestamp'].columns, has_item('number_of_unique_users'))
		assert_that(data['df_by_timestamp'].columns, has_item('number_of_topics_created'))
		assert_that(data['df_by_timestamp'].columns, has_item('ratio'))
		total_topics_created = np.sum(data['df_by_timestamp']['number_of_topics_created'])

		context_df = data['df_per_course_sections']
		total_events = np.sum(context_df['number_of_topics_created'])
		assert_that(total_events, equal_to(total_topics_created))
		assert_that(total_events, equal_to(len(tct.dataframe.index)))