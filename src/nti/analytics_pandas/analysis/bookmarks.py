#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ..queries import QueryBookmarksCreated

from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

class BookmarkCreationTimeseries(object):
	"""
	analyze the number of bookmarks creation given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		qbc = self.query_bookmarks_created = QueryBookmarksCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qbc.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qbc.filter_by_period_of_time(start_date, end_date)

	def explore_number_of_events_based_timestamp_date(self):
		events_df = explore_number_of_events_based_timestamp_date_(self.dataframe)
		if events_df is not None :
			events_df.rename(columns={'index':'total_bookmarks_created'}, inplace=True)
		return events_df

	def explore_unique_users_based_timestamp_date(self):
		unique_users_per_period_df = explore_unique_users_based_timestamp_date_(self.dataframe)
		return unique_users_per_period_df

	def explore_ratio_of_events_over_unique_users_based_timestamp_date(self):
		events_df = self.explore_number_of_events_based_timestamp_date()
		unique_users_df = self.explore_unique_users_based_timestamp_date()
		merge_df = explore_ratio_of_events_over_unique_users_based_timestamp_date_(
										events_df, 'total_bookmarks_created', unique_users_df)
		return merge_df
