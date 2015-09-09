#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import pandas as pd

from ..queries import QueryCourseCatalogViews
from ..queries import QueryCourseEnrollments
from ..queries import QueryCourseDrops

from .common_analysis_methods import add_timestamp_period_date
from .common_analysis_methods import explore_unique_users_based_timestamp_date_
from .common_analysis_methods import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class CourseCatalogViewsTimeseries(object):
	"""
	analyze the number of course catalog views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qccv = self.query_course_catalog_views = QueryCourseCatalogViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qccv.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qccv.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		df = add_timestamp_period_date(self.dataframe)
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		timestamp_period_df = grouped.aggregate(pd.Series.nunique)
		timestamp_period_df.rename(columns={'index':'total_course_catalog_views'}, inplace=True)
		return timestamp_period_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, 'total_course_catalog_views', unique_users_df)
		return merge_df


class CourseEnrollmentsTimeseries(object):
	"""
	analyze the number of course enrollments given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qce = self.query_course_enrollments = QueryCourseEnrollments(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qce.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qce.filter_by_period_of_time(start_date, end_date)
	
	def explore_number_of_events_based_timestamp_date(self):
		df = add_timestamp_period_date(self.dataframe)
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		events_df = grouped.aggregate(pd.Series.nunique)
		events_df.rename(columns={'index':'total_enrollments'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, 'total_enrollments', unique_users_df)
		return merge_df

class CourseDropsTimeseries(object):
	"""
	analyze the number of course drops given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qce = self.query_course_enrollments = QueryCourseEnrollments(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qce.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qce.filter_by_period_of_time(start_date, end_date)
	
	def explore_number_of_events_based_timestamp_date(self):
		df = add_timestamp_period_date(self.dataframe)
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		events_df = grouped.aggregate(pd.Series.nunique)
		events_df.rename(columns={'index':'total_enrollments'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, 'total_enrollments', unique_users_df)
		return merge_df

class CourseDropsTimeseries(object):
	"""
	analyze the number of course drops given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qcd = self.query_course_drops = QueryCourseDrops(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qcd.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qcd.filter_by_period_of_time(start_date, end_date)
	
	def explore_number_of_events_based_timestamp_date(self):
		df = add_timestamp_period_date(self.dataframe)
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		events_df = grouped.aggregate(pd.Series.nunique)
		events_df.rename(columns={'index':'total_drops'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df, 'total_drops', unique_users_df)
		return merge_df





