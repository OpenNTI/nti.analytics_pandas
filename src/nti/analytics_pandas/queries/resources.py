#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: videos.py 72636 2015-09-09 15:04:50Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics.database.resources import Resources

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryResources(TableQueryMixin):

	table = Resources

	def get_all_resources(self):
		r = self.table
		query = self.session.query(	r.resource_id,
									r.resource_ds_id,
									r.resource_display_name,
									r.max_time_length)
		dataframe = orm_dataframe(query, self.columns)
		print(dataframe.head())
		return dataframe

	def get_resources_ds_id_given_id(self, resource_id=()):
		r = self.table
		query = self.session.query(	r.resource_id,
									r.resource_ds_id).filter(r.resource_id.in_(resource_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_resources_given_id(self, resources_id=()):
		r = self.table
		query = self.session.query(	r.resource_id,
									r.resource_ds_id,
									r.resource_display_name,
									r.max_time_length).filter(r.resource_id.in_(resources_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe		

	
