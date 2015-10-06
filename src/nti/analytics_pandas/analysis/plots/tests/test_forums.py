#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.forums import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCommentsCreatedTimeseries

from nti.analytics_pandas.analysis.plots.forums import ForumsCreatedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCommentsCreatedTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestForumsCreatedPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestForumsCreatedPlot, self).setUp()

	def test_explore_events_forums_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.explore_events()

	def test_analyze_device_types_plot(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.analyze_device_types()

class TestForumCommentsCreatedPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestForumCommentsCreatedPlot, self).setUp()

	def test_explore_events_forums_comments_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.explore_events()

	def test_analyze_device_types_forums_comments_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_  = fcctp.analyze_device_types()
