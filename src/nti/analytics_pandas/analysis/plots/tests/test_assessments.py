#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.assessments import AssignmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import AssignmentsTakenTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentViewsTimeseries
from nti.analytics_pandas.analysis.plots.assessments import AssignmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import AssignmentsTakenTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import SelfAssessmentViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestAssignmentViewsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestAssignmentViewsPlot, self).setUp()

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_group_by_device_type(period_breaks='1 day', minor_period_breaks=None)


class TestAssignmentsTakenPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestAssignmentsTakenPlot, self).setUp()

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_group_by_device_type(period_breaks='1 week', minor_period_breaks='1 day')


class TestSelfAssessmentViewsPlot(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestSelfAssessmentViewsPlot, self).setUp()

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_group_by_device_type(period_breaks='1 day', minor_period_breaks=None)
