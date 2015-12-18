#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.profile_views import EntityProfileViewsTimeseries

from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileViewsTimeseriesPlot


from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestProfileViewsPlot(AnalyticsPandasTestBase):
	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.explore_events()
		assert_that(len(_), equal_to(3))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.analyze_application_types()
		assert_that(len(_), equal_to(3))