#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.enrollments import CourseCatalogViewsTimeseries
from nti.analytics_pandas.analysis.plots.enrollments import CourseCatalogViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourseCatalogViewsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestCourseCatalogViewsPlot, self).setUp()

	def test_explore_events_course_catalog_views(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.explore_events()
