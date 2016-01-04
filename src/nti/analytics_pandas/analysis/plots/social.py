#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: social.py 78747 2015-12-10 15:54:52Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from .commons import line_plot_x_axis_date
from .commons import generate_three_plots
from .commons import generate_three_group_by_plots

class ContactsEventsTimeseriesPlot(object):
	def __init__(self, cet):
		"""
		cet = ContactsEventsTimeseries
		"""
		self.cet = cet

	def combine_events(self, 
					   period_breaks=None,
					   minor_period_breaks=None,
					   theme_seaborn_=True):
		cet = self.cet
		df = cet.combine_events()
		group_by = 'event_type'
		event_title = _('Number of contact related events grouped by event type during period of time')
		user_title = _('Number of unique users creating contact events during period of time')
		ratio_title = _('Ratio of contact related events over unique user on each available date')
		event_type = 'event_type'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of contact related events')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=cet.period)
		return plots

