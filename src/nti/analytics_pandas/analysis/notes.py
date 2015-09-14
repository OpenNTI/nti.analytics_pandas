#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryNoteLikes
from ..queries import QueryNotesViewed
from ..queries import QueryNotesCreated
from ..queries import QueryNoteFavorites

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class NotesCreationTimeseries(object):
	"""
	analyze the number of notes created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type = True, with_device_type = True):
		self.session = session
		qnc = self.query_notes_created = QueryNotesCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnc.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qnc.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qnc.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_resource_type:
			new_df = qnc.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df


	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_notes_created'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_notes_created', unique_users_df)
		return merge_df

class NotesViewTimeseries(object):
	"""
	analyze the number of notes viewed given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type=True, with_device_type=True):
		self.session = session
		qnv = self.query_notes_viewed = QueryNotesViewed(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnv.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qnv.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qnv.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_resource_type:
			new_df = qnv.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_notes_viewed'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_notes_viewed', unique_users_df)
		return merge_df

class NoteLikesTimeseries(object):
	"""
	analyze the number of note likes given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type=True, with_device_type=True):
		self.session = session
		qnl = self.query_notes_viewed = QueryNoteLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnl.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qnl.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qnl.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_resource_type:
			new_df = qnl.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_note_likes'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
												events_df, 'total_note_likes', unique_users_df)
		return merge_df

class NoteFavoritesTimeseries(object):
	"""
	analyze the number of note favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None, with_resource_type=True, with_device_type=True):
		self.session = session
		qnf = self.query_notes_viewed = QueryNoteFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnf.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qnf.filter_by_period_of_time(start_date, end_date)

		if with_device_type:
			new_df = qnf.add_device_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

		if with_resource_type:
			new_df = qnf.add_resource_type(self.dataframe)
			if new_df is not None: 
				self.dataframe = new_df

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_note_favorites'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
											events_df, 'total_note_favorites', unique_users_df)
		return merge_df
