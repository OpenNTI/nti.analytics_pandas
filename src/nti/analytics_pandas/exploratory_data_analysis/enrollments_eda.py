#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: enrollments_eda.py 72519 2015-09-08 08:38:51Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from ..queries.enrollments import QueryCourseCatalogViews
import pandas as pd
from .import add_timestamp_period_date

class CourseCatalogViewsTimeseries(object):
	"""
	analyze the number of course catalog views given time period and list of course id
	"""
	def __init__(self, session, start_date, end_date, course_id=None):
		self.session = session
		self.query_course_catalog_views = QueryCourseCatalogViews(self.session)
		qccv= self.query_course_catalog_views
		if isinstance (course_id, list):
			self.dataframe = qccv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		else :
			self.dataframe = qccv.filter_by_period_of_time(start_date,end_date)

	def explore_number_of_events_based_timestamp_date(self):
		df = add_timestamp_period_date(self.dataframe)
		grouped = df.groupby('timestamp_period')
		timestamp_period_df = grouped.aggregate(pd.Series.nunique)
		timestamp_period_df.rename(columns = {'index':'total_course_catalog_views'}, inplace=True)
		return timestamp_period_df