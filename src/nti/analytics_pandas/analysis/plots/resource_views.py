#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: resource_views.py 73525 2015-09-23 19:15:51Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd
import matplotlib.pyplot as plt

class  ResourceViewsTimeseriesPlot(object):
	
	def __init__(self, rvt):
		"""
		rvt = ResourceViewsTimeseries
		"""
		self.rvt = rvt

	def explore_events(self):
		"""
		return line chart of the number of resource views during period of time 
		it consists of :
			- number of resource views 
			- number of unique users 
			- ratio of resource views over unique users 
		"""
		rvt = self.rvt
		df = rvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		plt.figure()
		figure = df.plot().get_figure()
		return figure
