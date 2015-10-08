#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries
from nti.analytics_pandas.analysis.plots.notes import NotesCreationTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestNotesCreationPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestNotesCreationPlot, self).setUp()

	def test_explore_events_bookmark_creation(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.explore_events()

	def test_analyze_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_device_types()

	def test_analyze_resource_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_resource_types()