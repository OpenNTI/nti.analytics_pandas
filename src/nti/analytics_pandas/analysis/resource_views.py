#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryCourseResourceViews

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class ResourceViewsTimeseries(object):
	"""
	analyze the number of resource views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type=True, with_device_type=True):
		self.session = session
		qrv = self.query_resources_view = QueryCourseResourceViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qrv.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qrv.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qrv.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_resource_type:
			new_df = qrv.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_resource_views'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_resource_views', unique_users_df)
		return merge_df
