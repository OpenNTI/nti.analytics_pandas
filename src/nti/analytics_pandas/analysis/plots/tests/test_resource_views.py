#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.resource_views import ResourceViewsTimeseries
from nti.analytics_pandas.analysis.plots.resource_views import ResourceViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViewsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestResourceViewsPlot, self).setUp()

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		_ = rvtp.explore_events()

	def test_resource_and_device_type_analysis(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		_ = rvtp.analyze_resource_type()
		_ = rvtp.analyze_device_type()

	def test_process_analysis_by_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		_ = rvtp.analyze_events_based_on_resource_device_type()

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		_ = rvtp.plot_most_active_users()
