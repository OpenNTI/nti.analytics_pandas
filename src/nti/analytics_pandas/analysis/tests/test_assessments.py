#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.assessments import AssignmentViewsTimeseries

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