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

from .commons import build_plot_images_dictionary_

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class ResourceViewsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				period_breaks=None, minor_period_breaks=None, theme_seaborn_=True):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_seaborn_ = theme_seaborn_
		self.minor_period_breaks = minor_period_breaks

Context = ResourceViewsTimeseriesContext

class ResourceViewsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Resource Views')

	def _build_data(self, data=_('sample resource views report')):
		self.options['data'] = data
		return self.options

	def __call__(self):
		self.rvt = ResourceViewsTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses)
		self.rvtp = ResourceViewsTimeseriesPlot(self.rvt)
		data = {}
		data = self.get_resource_view_events(data)
		self._build_data(data)
		return self.options

	def get_resource_view_events(self, data):
		plots = self.rvtp.explore_events(self.context.period_breaks,
									self.context.minor_period_breaks,
									self.context.theme_seaborn_)
		data['resource_view_events'] = None
		if plots is not None and len(plots) > 0 :
			data['resource_view_events'] = build_plot_images_dictionary_(plots)
		return data

View = ResourceViewsTimeseriesReport = ResourceViewsTimeseriesReportView
