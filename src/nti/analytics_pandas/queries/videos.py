#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_views import VideoEvents

from nti.common.property import Lazy

from . import orm_dataframe

class VideosMixin(object):

	table = None

	def __init__(self, session):
		self.session = session

	@Lazy
	def columns(self):
		table = getattr(self.table, '__table__')
		return table.columns.keys()

class QueryVideoEvents(VideosMixin):

	table = VideoEvents

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ve = self.table
		query = self.session.query( ve.video_view_id,
									ve.timestamp,
									ve.course_id,
									ve.resource_id,
									ve.context_path,
									ve.time_length,
									ve.video_event_type,
									ve.video_start_time,
									ve.video_end_time,
									ve.with_transcript,
									ve.session_id,
									ve.user_id,
									ve.play_speed).filter(ve.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
