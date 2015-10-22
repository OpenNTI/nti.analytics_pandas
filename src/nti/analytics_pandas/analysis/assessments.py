#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: assessments.py 74275 2015-10-07 14:52:41Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np
import pandas as pd

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_
from .common import explore_unique_users_based_timestamp_date_
from .common import explore_number_of_events_based_timestamp_date_
from .common import explore_ratio_of_events_over_unique_users_based_timestamp_date_

from ..queries import QueryAssignmentViews
from ..queries import QueryAssignmentsTaken
from ..queries import QuerySelfAssessmentViews
from ..queries import QuerySelfAssessmentsTaken

from ..utils import cast_columns_as_category_

class AssignmentViewsTimeseries(object):
	"""
	analyze the number of assignment views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True, time_period_date=True):

		self.session = session
		qav = self.query_assignment_view = QueryAssignmentViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qav.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else :
			self.dataframe = qav.filter_by_period_of_time(start_date, end_date)

		if with_resource_type:
			new_df = qav.add_resource_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if with_device_type:
			new_df = qav.add_device_type(self.dataframe)
			if new_df is not None:
				self.dataframe = new_df

		if time_period_date :
			self.dataframe = add_timestamp_period_(self.dataframe)

		categorical_columns = ['assignment_view_id', 'user_id', 'device_type', 'resource_type']
		self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains :
		 - the number of assignment views, 
		 - the number of unique user viewing assignment 
		 - ratio of assignment views over unique users 
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		agg_columns = {	'assignment_view_id': pd.Series.count,
						'user_id'			: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		df.rename(columns={	'assignment_view_id':'number_assignment_viewed',
							'user_id'			:'number_of_unique_users'},
					inplace=True)
		df['ratio'] = df['number_assignment_viewed'] / df['number_of_unique_users']
		return df