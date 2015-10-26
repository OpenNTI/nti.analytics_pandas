#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryVideoEvents

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import add_timestamp_period_

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
		else:
			self.dataframe = qve.filter_by_period_of_time(start_date, end_date)
		
		categorical_columns = ['video_event_type', 'with_transcript']
		
		self.with_device_type = with_device_type
		if with_device_type:
			new_df = qve.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df
				categorical_columns.append('device_type')

		if time_period_date:
			self.dataframe = add_timestamp_period_(self.dataframe)

		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_video_events(self):
		group_by_items=['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_video_events_types(self):
		group_by_items = ['timestamp_period', 'video_event_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'user_id': pd.Series.nunique,
						'video_view_id': pd.Series.count}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		df.rename(columns={	'user_id'		:'number_of_unique_users',
							'video_view_id'	:'number_of_video_events'},
					inplace=True)
		df['ratio'] = df['number_of_video_events'] / df['number_of_unique_users']
		return df