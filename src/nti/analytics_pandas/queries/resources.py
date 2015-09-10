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
		return dataframe

	def get_resources_ds_id_given_id(self, resource_id=()):
		r = self.table
		query = self.session.query(	r.resource_id,
									r.resource_ds_id).filter(r.resource_id.in_(resource_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_resources_given_id(self, resources_id=None):
		r = self.table
		query = self.session.query(	r.resource_id,
									r.resource_ds_id,
									r.resource_display_name,
									r.max_time_length).filter(r.resource_id.in_(resources_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe		

	def add_resource_type(self, dataframe):
		def label_resource_type(resource_ds_id):
			if u'.ntivideo.' in resource_ds_id:
				return u'video'
			elif u'NTISlideVideo' in resource_ds_id:
				return u'slide video'
			elif u'.relatedworkref.' in resource_ds_id:
				if u'requiredreadings' in resource_ds_id :
					return u'required readings'
				elif u'textbook' in resource_ds_id:
					return u'textbook'
				elif u'reading_' in resource_ds_id:
					return u'reading'
				elif u'lecture' in resource_ds_id:
					return u'related work lecture'
				else:
					return u'unknown relatedworkref'
			elif u'naq.asg.assignment:' in resource_ds_id:
				return u'assignment'
			elif u'naq.set.qset' in resource_ds_id:
				return u'question set'
			elif u'.naq.qid.' in resource_ds_id:
				if u'self_check' in resource_ds_id:
					return u'self_check'
				elif u'quiz' in resource_ds_id:
					return u'quiz'
				else : 
					return u'naq_qid'
			elif u'self_assessment' in resource_ds_id:
				return u'self assessment'
			elif u'honor_code' in resource_ds_id:
				return u'honor code'
			elif u'lec:' in resource_ds_id:
				return u'lecture'
			elif u'reading:' in resource_ds_id:
				return u'reading'
			elif u'discussion:' in resource_ds_id or u'discussions:' in resource_ds_id:
				return u'discussion'
			elif u'In_Class_Discussions' in resource_ds_id:
				return u'in class discussion'
			elif u'section:' in resource_ds_id or u'sec:' in resource_ds_id:
				return u'section'
			elif u'self_check' in resource_ds_id or 'check_yourself' in resource_ds_id:
				return u'self check'
			elif u'quiz' in resource_ds_id:
				return u'quiz'
			elif u'pre_lab_workbook:' in resource_ds_id:
				return u'pre lab workbook'
			elif u'nticard' in resource_ds_id:
				return u'nticard'
			elif u'JSON:Timeline' in resource_ds_id:
				return u'timeline'
 			else:
				return u'unknown'

		dataframe['resource_type'] = dataframe['resource_ds_id'].apply(lambda x: label_resource_type(x))
		return dataframe
	
