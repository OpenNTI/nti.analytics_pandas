#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryAssignmentViews
from ..queries import QueryAssignmentsTaken
from ..queries import QueryCourseEnrollments
from ..queries import QuerySelfAssessmentViews
from ..queries import QuerySelfAssessmentsTaken

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import add_timestamp_period_

class AssessmentEventsTimeseries(object):

	def __init__(self, avt=None, att=None, savt=None, satt=None):
		"""
		avt = AssignmentViewsTimeseries
		att = AssignmentsTakenTimeseries
		savt = SelfAssessmentViewsTimeseries
		satt = SelfAssessmentsTakenTimeseries
		"""
		self.avt = avt
		self.att = att
		self.savt = savt
		self.satt = satt

	def combine_events(self):
		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'event_type'])
		if self.avt is not None:
			avt = self.avt
			assignment_views_df = avt.analyze_events()
			assignment_views_df = self.update_events_dataframe(assignment_views_df,
				column_to_rename='number_assignments_viewed',
				event_type='Assignment View')
			df = df.append(assignment_views_df)

		if self.att is not None:
			att = self.att
			assignments_taken_df = att.analyze_events()
			assignments_taken_df = self.update_events_dataframe(assignments_taken_df,
				column_to_rename='number_assignments_taken',
				event_type='Assignment Taken')
			df = df.append(assignments_taken_df)

		if self.savt is not None:
			savt = self.savt
			self_assessment_views_df = savt.analyze_events()
			self_assessment_views_df = self.update_events_dataframe(self_assessment_views_df,
				column_to_rename='number_self_assessments_viewed',
				event_type='Self Asst. View')
			df = df.append(self_assessment_views_df)

		if self.satt is not None:
			satt = self.satt
			self_assessments_taken_df = satt.analyze_events()
			self_assessments_taken_df = self.update_events_dataframe(self_assessments_taken_df,
				column_to_rename='number_self_assessments_taken',
				event_type='Self Asst. Taken')
			df = df.append(self_assessments_taken_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

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
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_resource_type(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
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
				 with_resource_type=True, with_device_type=True,
				 time_period_date=True, with_assignment_title=True):

		self.session = session
		self.course_id = course_id
		qat = self.query_assignments_taken = QueryAssignmentsTaken(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qat.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qat.filter_by_period_of_time(start_date, end_date)

		categorical_columns = ['assignment_taken_id', 'user_id']

		if with_device_type:
			new_df = qat.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('device_type')

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		if with_assignment_title:
			new_df = qat.add_assignment_title(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('assignment_title')

		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains:
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'assignment_taken_id'	: pd.Series.count,
						'user_id'				: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'assignment_taken_id'	:'number_assignments_taken',
							'user_id'				:'number_of_unique_users'},
				  inplace=True)
		df['ratio'] = df['number_assignments_taken'] / df['number_of_unique_users']
		return df

	def analyze_assignment_taken_over_total_enrollments(self):
		dataframe = self.dataframe[['assignment_title', 'assignment_taken_id']]
		group_by_columns = ['assignment_title']
		agg_columns = {'assignment_taken_id' : pd.Series.count}

		df = analyze_types_(dataframe, group_by_columns, agg_columns)
		df.rename(columns={'assignment_taken_id' :'number_assignments_taken'}, inplace=True)

		qce = QueryCourseEnrollments(self.session)
		total_enrollments = qce.count_enrollments(self.course_id)

		df['ratio'] = df['number_assignments_taken'] / total_enrollments

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
		else:
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
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		grouped by device type on each available date
		"""
		if 'device_type' in self.dataframe.columns:
			group_by_columns = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_columns)
			return df

	def analyze_events_group_by_resource_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		grouped by device type on each available date
		"""
		if 'resource_type' in self.dataframe.columns:
			group_by_columns = ['timestamp_period', 'resource_type']
			df = self.build_dataframe(group_by_columns)
			return df

	def build_dataframe(self, group_by_columns):
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
		else:
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
		return a dataframe contains:
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'self_assessment_id'	: pd.Series.count,
						'user_id'				: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'self_assessment_id'	:'number_self_assessments_taken',
							'user_id'				:'number_of_unique_users'},
					inplace=True)
		df['ratio'] = df['number_self_assessments_taken'] / df['number_of_unique_users']
		return df
