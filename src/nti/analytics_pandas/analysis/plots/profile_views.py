#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: profile_views.py 78747 2015-12-10 15:54:52Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

import numpy as np

from zope.i18n import translate

from .commons import line_plot_x_axis_date
from .commons import generate_three_plots
from .commons import generate_three_group_by_plots

class EntityProfileViewsTimeseriesPlot(object):

	def __init__(self, epvt):
		"""
		epvt = EntityProfileViewsTimeseries
		"""
		self.epvt = epvt
		self.period = epvt.period

	def explore_events(self, period_breaks=None, minor_period_breaks=None,
					   theme_seaborn_=True):
		epvt = self.epvt
		df = epvt.analyze_events()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of profile views')
		user_title = _("Number of unique users viewing profiles")
		ratio_title = _("Ratio of profile views over unique user")
		
		event_type = 'profile_views'
		event_y_axis_field = 'number_of_profile_views'
		event_y_axis_label = _('Number of profile views')

		plots = generate_three_plots(df,
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

