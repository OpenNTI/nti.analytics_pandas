#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.exploratory_data_analysis.enrollments_eda import CourseCatalogViewsTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

import numpy as np

class TestCourseCatalogViewsEDA(AnalyticsPandasTestBase):
	def setUp(self):
		super(TestCourseCatalogViewsEDA, self).setUp()

	def test_course_catalog_views_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		
		events_df = ccvt.explore_number_of_events_based_timestamp_date()
		assert_that(len(events_df.index), equal_to(109))
		total_events = np.sum(events_df['total_course_catalog_views'])
		assert_that(total_events, equal_to(409))

