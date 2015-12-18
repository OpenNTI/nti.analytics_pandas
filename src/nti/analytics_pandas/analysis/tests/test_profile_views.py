#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.profile_views import EntityProfileViewsTimeseries
from nti.analytics_pandas.analysis.profile_views import EntityProfileActivityViewsTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestEntityProfileViewsTimeseries(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		assert_that(epvt.dataframe, has_item('timestamp'))
		assert_that(epvt.dataframe, has_item('timestamp_period'))
		assert_that(epvt.dataframe, has_item('target_id'))
		assert_that(epvt.dataframe, has_item('user_id'))

		df = epvt.analyze_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_profile_views'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		df = epvt.analyze_application_types()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('application_type'))
		assert_that(df.columns, has_item('number_of_profile_views'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_get_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		df = epvt.get_the_most_active_users()
		assert_that(df.columns, has_item('number_of_profile_views'))

	def test_get_the_most_viewed_profiles(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		df = epvt.get_the_most_viewed_profiles()
		assert_that(df.columns, has_item('number_of_profile_viewed'))

class TestEntityProfileActivityViewsTimeseries(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		assert_that(epavt.dataframe, has_item('timestamp'))
		assert_that(epavt.dataframe, has_item('timestamp_period'))
		assert_that(epavt.dataframe, has_item('target_id'))
		assert_that(epavt.dataframe, has_item('user_id'))

		df = epavt.analyze_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_profile_activity_views'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		df = epavt.analyze_application_types()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('application_type'))
		assert_that(df.columns, has_item('number_of_profile_activity_views'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_get_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		df = epavt.get_the_most_active_users()
		assert_that(df.columns, has_item('number_of_profile_activity_views'))

	def test_get_the_most_viewed_profiles(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		df = epavt.get_the_most_viewed_profile_activities()
		assert_that(df.columns, has_item('number_of_profile_activity_viewed'))
