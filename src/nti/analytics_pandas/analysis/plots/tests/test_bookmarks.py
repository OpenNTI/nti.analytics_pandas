#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.bookmarks import BookmarkCreationTimeseries
from nti.analytics_pandas.analysis.plots.bookmarks import BookmarksTimeseriesPlot 

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestBookmarksPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestBookmarksPlot, self).setUp()

	def test_explore_events_bookmark_creation(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.explore_events()

	def test_analyze_bookmark_creation_resource_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.analyze_resource_types()
