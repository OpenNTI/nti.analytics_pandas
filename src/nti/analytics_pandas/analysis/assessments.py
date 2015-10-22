#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from .common import analyze_types_
from .common import add_timestamp_period_

from ..queries import QueryAssignmentViews
from ..queries import QueryAssignmentsTaken
from ..queries import QuerySelfAssessmentViews
from ..queries import QuerySelfAssessmentsTaken

from ..utils import cast_columns_as_category_

class AssignmentViewsTimeseries(object):
	"""
	analyze the number of assignment views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):

		self.session = session
		qav = self.query_assignment_view = QueryAssignmentViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qav.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qav.filter_by_period_of_time(start_date, end_date)

		categorical_columns = ['assignment_view_id', 'user_id']

		if with_resource_type:
			new_df = qav.add_resource_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('resource_type')

		if with_device_type:
			new_df = qav.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('device_type')

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains :
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		agg_columns = {	'assignment_view_id': pd.Series.count,
						'user_id'			: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'assignment_view_id':'number_assignments_viewed',
							'user_id'			:'number_of_unique_users'},
				  inplace=True)
		df['ratio'] = df['number_assignments_viewed'] / df['number_of_unique_users']
		return df

class AssignmentsTakenTimeseries(object):
	"""
	analyze the number of assignments taken given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):

		self.session = session
		qat = self.query_assignments_taken = QueryAssignmentsTaken(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qat.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qat.filter_by_period_of_time(start_date, end_date)

		categorical_columns = ['assignment_taken_id', 'user_id']

		if with_device_type:
			new_df = qat.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('device_type')

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains :
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		agg_columns = {	'assignment_taken_id'	: pd.Series.count,
						'user_id'				: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'assignment_taken_id'	:'number_assignments_taken',
							'user_id'				:'number_of_unique_users'},
				  inplace=True)
		df['ratio'] = df['number_assignments_taken'] / df['number_of_unique_users']
		return df

class SelfAssessmentViewsTimeseries(object):
	"""
	analyze the number of self assessments views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):

		self.session = session
		qsav = self.query_self_assessment_view = QuerySelfAssessmentViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qsav.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qsav.filter_by_period_of_time(start_date, end_date)

		categorical_columns = ['self_assessment_view_id', 'user_id']
		if with_resource_type:
			new_df = qsav.add_resource_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('resource_type')

		if with_device_type:
			new_df = qsav.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('device_type')

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		categorical_columns = ['self_assessment_view_id', 'user_id', 'device_type']
		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains :
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		agg_columns = {	'self_assessment_view_id'	: pd.Series.count,
						'user_id'					: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'self_assessment_view_id'	:'number_self_assessments_viewed',
							'user_id'					:'number_of_unique_users'},
				  inplace=True)
		df['ratio'] = df['number_self_assessments_viewed'] / df['number_of_unique_users']
		return df

class SelfAssessmentsTakenTimeseries(object):
	"""
	analyze the number of self assessments taken given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):

		self.session = session
		qsat = self.query_self_assessments_taken = QuerySelfAssessmentsTaken(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qsat.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qsat.filter_by_period_of_time(start_date, end_date)

		categorical_columns = ['self_assessment_id', 'user_id']

		if with_device_type:
			new_df = qsat.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('device_type')

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains :
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		agg_columns = {	'self_assessment_id'	: pd.Series.count,
						'user_id'				: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'self_assessment_id'	:'number_self_assessments_taken',
							'user_id'				:'number_of_unique_users'},
					inplace=True)
		df['ratio'] = df['number_self_assessments_taken'] / df['number_of_unique_users']
		return df
