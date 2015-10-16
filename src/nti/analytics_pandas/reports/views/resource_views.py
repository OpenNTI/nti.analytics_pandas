#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from ...analysis import ResourceViewsTimeseries
from ...analysis import ResourceViewsTimeseriesPlot

from .mixins import AbstractReportView

class ResourceViewsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date

Context = ResourceViewsTimeseriesContext

class ResourceViewsTimeseriesReportView(AbstractReportView):

	def __init__(self, context):
		AbstractReportView.__init__(self, context=context)

	def _build_data(self, title=_('Resource Views')):
		self.options['title'] = title
		return self.options

	def __call__(self):
		self.rvt = ResourceViewsTimeseries(self.session,
										   self.start_date,
										   self.end_date,
										   self.courses)
		self.rvtp = ResourceViewsTimeseriesPlot(self.rvt)
		self._build_data()
		return self.options

View = ResourceViewsTimeseriesReport = ResourceViewsTimeseriesReportView
