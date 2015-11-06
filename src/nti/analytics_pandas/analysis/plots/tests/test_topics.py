#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.topics import TopicLikesTimeseries
from nti.analytics_pandas.analysis.topics import TopicViewsTimeseries
from nti.analytics_pandas.analysis.topics import TopicsEventsTimeseries
from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries
from nti.analytics_pandas.analysis.topics import TopicFavoritesTimeseries

from nti.analytics_pandas.analysis.plots.topics import TopicLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicsCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicFavoritesTimeseriesPlot

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
		_ = tctp.explore_events(period_breaks='1 day', minor_period_breaks='None')

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tctp = TopicsCreationTimeseriesPlot(tct)
		_ = tctp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks='None')

	def test_analyze_events_per_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tctp = TopicsCreationTimeseriesPlot(tct)
		_ = tctp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks='None')

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

	def test_analyze_device_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.analyze_device_types(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks='None')

	def test_plot_the_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.plot_the_most_active_users()

class TestTopicLikesPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicLikesPlot, self).setUp()

	def test_explore_events_topics_viewed(self):
		start_date = '2015-10-05'
		end_date = '2015-10-27'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tltp = TopicLikesTimeseriesPlot(tlt)
		_ = tltp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-27'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tltp = TopicLikesTimeseriesPlot(tlt)
		_ = tltp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-10-27'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tltp = TopicLikesTimeseriesPlot(tlt)
		_ = tltp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

class TestTopicFavoritesPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicFavoritesPlot, self).setUp()

	def test_explore_events_topics_viewed(self):
		start_date = '2015-10-05'
		end_date = '2015-10-27'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		tftp = TopicFavoritesTimeseriesPlot(tft)
		_ = tftp.explore_events(period_breaks='1 day', minor_period_breaks=None)

class TestTopicsEventsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestTopicsEventsPlot, self).setUp()

	def test_topics_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		tet = TopicsEventsTimeseries(tct, tvt, tlt, tft)
		tetp = TopicsEventsTimeseriesPlot(tet)
		_ = tetp.explore_all_events(period_breaks='1 week', minor_period_breaks='1 day')
