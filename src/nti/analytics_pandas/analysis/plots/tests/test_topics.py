#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries
from nti.analytics_pandas.analysis.topics import TopicViewsTimeseries
from nti.analytics_pandas.analysis.plots.topics import TopicsCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicViewsTimeseriesPlot
from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestTopicsCreationPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicsCreationPlot, self).setUp()

	def test_explore_events_topics_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tctp = TopicsCreationTimeseriesPlot(tct)
		_ = tctp.explore_events(period_breaks='1 week', minor_period_breaks='1 day')


class TestTopicViewsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicViewsPlot, self).setUp()

	def test_explore_events_topics_viewed(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.explore_events(period_breaks='1 week', minor_period_breaks='1 day')