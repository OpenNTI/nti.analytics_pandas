#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.highlights import HighlightsCreationTimeseries
from nti.analytics_pandas.analysis.plots.highlights import HighlightsCreationTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestHighlightsCreationPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestHighlightsCreationPlot, self).setUp()

	def test_explore_events_bookmark_creation(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		_ = hctp.explore_events()