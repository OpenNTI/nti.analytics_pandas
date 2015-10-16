#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.videos import VideoEventsTimeseries
from nti.analytics_pandas.analysis.plots.videos import VideoEventsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestVideoEventsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestVideoEventsPlot, self).setUp()

	def test_explore_events_topics_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.explore_events(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_video_events_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.analyze_video_events_types(period_breaks='1 week', minor_period_breaks='1 day')
