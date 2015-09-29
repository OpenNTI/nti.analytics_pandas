#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: resource_views.py 73213 2015-09-17 18:48:03Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .analysis import ResourceViewsTimeseriesPlot
from .analysis import ResourceViewsTimeseries

class ResourceViewsTimeseriesReport(object):
	def __init__(self, session, start_date, end_date, courses_id):
		self.rvt = rvt = ResourceViewsTimeseries(session, start_date, end_date, courses_id)
		self.rvtp = ResourceViewsTimeseriesPlot(rvt)

	def generate_events_plots(self):
		rvtp = self.rvtp	
		plot_resource_views, plot_unique_users, plot_ratio = rvtp.explore_events()
		#TODO : generate images on the fly and render them along with template to pdf
