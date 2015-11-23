#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np

from .courses import QueryCourses

from .resources import QueryResources

from .sessions import QuerySessions
from .sessions import QueryUserAgents

def add_resource_type_(session, dataframe):

	if 'resource_id' in dataframe.columns:
		resources_id = np.unique(dataframe['resource_id'].values.ravel())
		if len(resources_id) == 1 and resources_id[0] is None:
			return
		resources_id = resources_id[~np.isnan(resources_id)].tolist()
		qr = QueryResources(session)
		resources_df = qr.get_resources_ds_id_given_id(resources_id)
		resources_df = qr.add_resource_type(resources_df)
		resources_df = resources_df[['resource_id', 'resource_type']]
		new_df = dataframe.merge(resources_df, how='left')
		return new_df

def add_device_type_(session, dataframe):

	if 'session_id' in dataframe.columns:
		sessions_id = np.unique(dataframe['session_id'].values.ravel())
		if len(sessions_id) == 1 and sessions_id[0] is None :
			return
		sessions_id = sessions_id[~np.isnan(sessions_id)].tolist()
		qs = QuerySessions(session)
		session_df = qs.get_sessions_user_agent_id(sessions_id)

		user_agents_id = np.unique(session_df['user_agent_id'].values.ravel())
		if len(user_agents_id) == 1 and user_agents_id[0] is None :
			return
		user_agents_id = user_agents_id[~np.isnan(user_agents_id)].tolist()
		qua = QueryUserAgents(session)
		user_agent_df = qua.get_user_agents_by_id(user_agents_id)
		user_agent_df = qua.add_device_type(user_agent_df)

		new_df = dataframe.merge(session_df, how='left').merge(user_agent_df, how='left')
		return new_df

def add_context_name_(session, dataframe, course_ids):
	if 'course_id' in dataframe.columns:
		qc = QueryCourses(session)
		context_df = qc.get_context_name(course_ids)
		context_df.rename(columns={'context_id':'course_id'}, inplace=True)
		new_df = dataframe.merge(context_df, how='left')
		return new_df

def add_enrollment_type_(session, dataframe, course_ids):
	if 'user_id' not in dataframe.columns:
		return
	users_id = np.unique(dataframe['user_id'].values.ravel())
	if len(users_id) == 1 and users_id[0] is None:
		return
	users_id = users_id[~np.isnan(users_id)].tolist()

	from .enrollments import QueryCourseEnrollments
	qce = QueryCourseEnrollments(session)
	enrollments_df = qce.filter_by_course_id_user_id(course_ids, users_id)

	types_id = np.unique(enrollments_df['type_id'].values.ravel())
	if len(types_id) == 1 and types_id[0] is None:
		return
	types_id = types_id[~np.isnan(types_id)].tolist()	
	from .enrollments import QueryEnrollmentTypes
	qet = QueryEnrollmentTypes(session)
	enrollment_types_df = qet.get_enrollment_types_given_type_id(types_id)
	enrollment_types_df.rename(columns={'type_name':'enrollment_type'}, inplace=True)

	new_df = dataframe.merge(enrollments_df, how='left').merge(enrollment_types_df, how='left')
	return new_df
	




