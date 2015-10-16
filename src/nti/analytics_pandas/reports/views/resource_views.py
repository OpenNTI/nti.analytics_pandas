#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ...analysis import ResourceViewsTimeseries
from ...analysis import ResourceViewsTimeseriesPlot

from .mixins import AbstractReportView

class ResourceViewsTimeseriesReport(AbstractReportView):
	
	rvt = None
	rvtp = None

	def __init__(self, session=None, start_date=None, end_date=None, courses=None):
		AbstractReportView.__init__(self, context=self)
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		
	def __call__(self):
		if self.session is None:
			return
		self.rvt = ResourceViewsTimeseries(self.session, 
										   self.start_date, 
										   self.end_date, 
										   self.courses)
		self.rvtp = ResourceViewsTimeseriesPlot(self.rvt)
