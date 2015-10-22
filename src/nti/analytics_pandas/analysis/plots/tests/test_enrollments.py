#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.enrollments import CourseDropsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseEnrollmentsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseCatalogViewsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseEnrollmentsEventsTimeseries
from nti.analytics_pandas.analysis.plots.enrollments import CourseDropsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseEnrollmentsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseCatalogViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseEnrollmentsEventsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourseCatalogViewsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestCourseCatalogViewsPlot, self).setUp()

	def test_explore_events_course_catalog_views(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.explore_events()

	def test_analyze_device_types_plot(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.analyze_device_types()

class TestCourseEnrollmentsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestCourseEnrollmentsPlot, self).setUp()

	def test_explore_events_course_enrollments(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cetp = CourseEnrollmentsTimeseriesPlot(cet)
		_ = cetp.explore_events()

	def test_analyze_device_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cetp = CourseEnrollmentsTimeseriesPlot(cet)
		_ = cetp.analyze_device_enrollment_types()

class TestCourseDropsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestCourseDropsPlot, self).setUp()

	def test_explore_events_course_drops(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.explore_events()

	def test_analyze_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.analyze_device_types()

	def test_analyze_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.analyze_enrollment_types()

class TestEnrollmentsEventsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestEnrollmentsEventsPlot, self).setUp()

	def test_enrollments_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		ceet = CourseEnrollmentsEventsTimeseries(cet, cdt)
		ceetp = CourseEnrollmentsEventsTimeseriesPlot(ceet)
		_ = ceetp.explore_course_enrollments_vs_drops()
