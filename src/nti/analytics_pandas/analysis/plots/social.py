#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: social.py 78747 2015-12-10 15:54:52Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd 

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

class ContactsAddedTimeseriesPlot(object):
	def __init__(self, cat):
		self.cat  = cat
		self.period = cat.period

	def analyze_events(self, 
					   period_breaks=None,
					   minor_period_breaks=None,
					   theme_seaborn_=True):
		cat = self.cat
		df = cat.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of contacts added during period of time')
		user_title = _('Number of unique users adding contacts during period of time')
		ratio_title = _('Ratio of contacts added over unique users during period of time')
		event_type = 'contacts_added'
		event_y_axis_field = 'number_of_contacts_added'
		event_y_axis_label = _('Number of contacts added')

		plots = generate_three_plots(
								 df,
								 event_title,
								 user_title,
								 ratio_title,
								 event_y_axis_field,
								 event_y_axis_label,
								 period_breaks,
								 minor_period_breaks,
								 theme_seaborn_,
								 event_type,
								 period=self.period)
		return plots

	def analyze_application_types(self,
								  period_breaks=None,
								  minor_period_breaks=None,
								  theme_seaborn_=True):
		cat = self.cat
		df = cat.analyze_application_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		
		group_by = 'application_type'
		event_title = _('Number of contacts added per application type')
		user_title = _('Number of unique users adding contacts per application type')
		ratio_title = _('Ratio of contacts added over unique users per application type')
		event_type = 'contacts_added_per_application_type'
		event_y_axis_field = 'number_of_contacts_added'
		event_y_axis_label = _('Number of contacts added')

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
											  period=self.period)
		return plots
