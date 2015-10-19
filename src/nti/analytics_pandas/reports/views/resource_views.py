#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import ResourceViewsTimeseries
from ...analysis import ResourceViewsTimeseriesPlot

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class ResourceViewsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date

Context = ResourceViewsTimeseriesContext

class ResourceViewsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Resource Views')
	
	def _build_data(self, data=_('sample')):
		self.options['data'] = data
		return self.options

	def __call__(self):
		self.rvt = ResourceViewsTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses)
		self.rvtp = ResourceViewsTimeseriesPlot(self.rvt)
		self._build_data()
		return self.options

View = ResourceViewsTimeseriesReport = ResourceViewsTimeseriesReportView
