#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics.database.resource_tags import NoteLikes
from nti.analytics.database.resource_tags import NotesViewed
from nti.analytics.database.resource_tags import NotesCreated
from nti.analytics.database.resource_tags import NoteFavorites

from nti.common.property import Lazy

from ..utils.orm_to_dataframe import orm_dataframe

class NotesMixin(object):

	table = None

	def __init__(self, session):
		self.session = session

	@Lazy
	def columns(self):
		table = getattr(self.table, '__table__')
		return table.columns.keys()

class QueryNotesCreated(NotesMixin):

	table = NotesCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nc = self.table
		query = self.session.query(nc.note_id,
								   nc.timestamp,
								   nc.course_id,
								   nc.resource_id,
								   nc.user_id,
								   nc.parent_user_id,
								   nc.session_id,
								   nc.sharing,
								   nc.favorite_count,
								   nc.like_count,
								   nc.note_length,
								   nc.is_flagged,
								   nc.deleted).filter(nc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryNotesViewed(NotesMixin):

	table = NotesViewed

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nv = self.table
		query = self.session.query(nv.note_id,
								   nv.timestamp,
								   nv.course_id,
								   nv.user_id,
								   nv.session_id,
								   nv.resource_id,
								   nv.context_path).filter(nv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryNoteFavorites(NotesMixin):

	table = NoteFavorites

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nf = self.table
		query = self.session.query(nf.note_id,
								   nf.timestamp,
								   nf.course_id,
								   nf.user_id,
								   nf.session_id,
								   nf.creator_id).filter(nf.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryNoteLikes(NotesMixin):

	table = NoteLikes

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nl = self.table
		query = self.session.query(nl.note_id,
								   nl.timestamp,
								   nl.course_id,
								   nl.user_id,
								   nl.session_id,
								   nl.creator_id).filter(nl.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe