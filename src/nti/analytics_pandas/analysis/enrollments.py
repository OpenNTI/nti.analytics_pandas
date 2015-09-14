#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryCourseDrops
from ..queries import QueryCourseEnrollments
from ..queries import QueryCourseCatalogViews
from ..queries import QueryEnrollmentTypes

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_
from .common import add_timestamp_period
from .common import analyze_types_

import pandas as pd
import numpy as np

class CourseCatalogViewsTimeseries(object):
	"""
	analyze the number of course catalog views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_device_type=True, time_period_date=True):
		self.session = session
		qccv = self.query_course_catalog_views = QueryCourseCatalogViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qccv.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qccv.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qccv.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df
		
		if time_period_date :
			self.dataframe = add_timestamp_period(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_course_catalog_views'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_course_catalog_views', unique_users_df)
		return merge_df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		agg_columns = {	'time_length'	: np.mean,
						'user_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={	'user_id'		:'number_of_unique_users',
							'time_length'	:'average_time_length'}, 
							inplace=True)
		return df


class CourseEnrollmentsTimeseries(object):
	"""
	analyze the number of course enrollments given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None, with_device_type=True, time_period_date=True, enrollment_type = True):
		self.session = session
		qce = self.query_course_enrollments = QueryCourseEnrollments(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qce.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qce.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qce.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if time_period_date :
			self.dataframe = add_timestamp_period(self.dataframe)

		if enrollment_type :
			qet =  QueryEnrollmentTypes(session)
			enrollment_type_df = qet.get_enrollment_types()
			self.dataframe = self.dataframe.merge(enrollment_type_df, how = 'left')

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_enrollments'}, inplace=True)
		events_df = events_df[['total_enrollments']]
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
												events_df, 'total_enrollments', unique_users_df)
		return merge_df

	def analyze_device_enrollment_types(self):
		group_by_items = ['timestamp_period', 'device_type', 'type_name']
		agg_columns = {	'user_id'    : pd.Series.nunique,
						'session_id' : pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={	'user_id':'number_of_unique_users'}, 
							inplace=True)
		return df

class CourseDropsTimeseries(object):
	"""
	analyze the number of course drops given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None, with_device_type=True, time_period_date=True):
		self.session = session
		qcd = self.query_course_drops = QueryCourseDrops(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qcd.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qcd.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qcd.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df
		if time_period_date :
			self.dataframe = add_timestamp_period(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_drops'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
												events_df, 'total_drops', unique_users_df)
		return merge_df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		agg_columns = {	'user_id'    : pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={	'user_id':'number_of_unique_users'}, 
							inplace=True)
		return df
