#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.assessments import AssignmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import AssignmentsTakenTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentsTakenTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestAssignmentViewsTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestAssignmentViewsTimeseries, self).setUp()

	def test_analyze_events(self):
		"""
		compare result with query :
		select count(assignment_view_id), date(timestamp)
		from AssignmentViews
		where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp)
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		df = avt.analyze_events()
		assert_that(len(df.index), equal_to(6))
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		df = avt.analyze_events_group_by_device_type()
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))
		
		df2 = avt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_group_by_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		df = avt.analyze_events_group_by_resource_type()
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))
		
		df2 = avt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

class TestAssignmentsTakenTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestAssignmentsTakenTimeseries, self).setUp()

	def test_analyze_events(self):
		"""
		compare result with query (running manually):
		select count(assignment_taken_id), date(timestamp)
		from AssignmentsTaken
		where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp)
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		df = att.analyze_events()
		assert_that(len(df.index), equal_to(129))
		assert_that(df.columns, has_item('number_assignments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

class TestSelfAssessmentViewsTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestSelfAssessmentViewsTimeseries, self).setUp()

	def test_analyze_events(self):
		"""
		compare result with query (running manually):
		select count(self_assessment_view_id), date(timestamp)
		from SelfAssessmentViews where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp);
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		df = savt.analyze_events()
		assert_that(len(df.index), equal_to(3))
		assert_that(df.columns, has_item('number_self_assessments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

class TestSelfAssessmentsTakenTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestSelfAssessmentsTakenTimeseries, self).setUp()

	def test_analyze_events(self):
		"""
		compare result with query (running manually):
		select count(self_assessment_id), date(timestamp)
		from SelfAssessmentsTaken where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp);
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date, end_date=end_date, course_id=courses_id)
		df = satt.analyze_events()
		assert_that(len(df.index), equal_to(85))
		assert_that(df.columns, has_item('number_self_assessments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))
