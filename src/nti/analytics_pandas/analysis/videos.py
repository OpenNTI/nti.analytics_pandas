#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryVideoEvents

from .common import add_timestamp_period_
from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class VideoEventsTimeseries(object):
	"""
	analyze the number of video events given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, time_period_date=True):
		self.session = session
		qve = self.query_videos_event = QueryVideoEvents(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qve.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qve.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qve.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date :
			self.dataframe = add_timestamp_period_(self.dataframe)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_video_events'}, inplace=True)
		events_df = events_df[['total_video_events']]
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_video_events', unique_users_df)
		return merge_df
