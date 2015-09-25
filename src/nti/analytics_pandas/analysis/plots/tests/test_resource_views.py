#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.resource_views import ResourceViewsTimeseries
from nti.analytics_pandas.analysis.plots.resource_views import ResourceViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViewsEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestResourceViewsEDA, self).setUp()

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		_ = rvtp.explore_events()
		# TODO : save the figure
		# figure.savefig('filepath')
