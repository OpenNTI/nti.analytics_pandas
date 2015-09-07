#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_views import VideoEvents

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryVideoEvents(TableQueryMixin):

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

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=[]):
		ve = self.table
		query = self.session.query( ve.video_view_id,
									ve.timestamp,
									ve.resource_id,
									ve.context_path,
									ve.time_length,
									ve.video_event_type,
									ve.video_start_time,
									ve.video_end_time,
									ve.with_transcript,
									ve.session_id,
									ve.user_id,
									ve.play_speed).filter(ve.timestamp.between(start_date, end_date)).filter(ve.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
