#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: bookmarks.py 78012 2015-12-01 18:08:53Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

import numpy as np

from zope.i18n import translate

from .commons import histogram_plot
from .commons import line_plot_x_axis_date
from .commons import generate_three_plots
from .commons import generate_three_group_by_plots


class ChatsTimeseriesPlot(object):

	def __init__(self, cit=None, cjt=None):
		"""
		cit = ChatsInitiatedTimeseries
		cjt = ChatsJoinedTimeseries
		"""
		self.cit = cit
		self.cjt = cjt

	def explore_chats_initiated(self, period_breaks='1 day', minor_period_breaks=None,
					  		 	theme_seaborn_=True):
		cit = self.cit
		if cit is None:
			return ()
		if cit.dataframe.empty:
			return ()
		df = cit.analyze_events()
		if df is None:
			return()
		event_title = _('Number of chats initiated during time period')
		user_title = _('Number of unique users initiating chats')
		ratio_title = _('Ratio of chats initiated over unique user on each available date')
		event_type = 'chats_initiated'
		event_y_axis_field = 'number_of_chats_initiated'
		event_y_axis_label = _('Number of chats initiated')

		plots = generate_three_plots(df,
									 event_title,
									 user_title,
									 ratio_title,
									 event_y_axis_field,
									 event_y_axis_label,
									 period_breaks,
									 minor_period_breaks,
									 theme_seaborn_,
									 event_type)

		return plots

	def analyze_application_types(self, period_breaks='1 day', minor_period_breaks=None,
					  		 	  theme_seaborn_=True):
		cit = self.cit
		if cit is None:
			return ()
		if cit.dataframe.empty:
			return ()
		df = cit.analyze_application_types()
		if df is None:
			return()
		group_by = 'application_type'
		event_title = _('Number of chats initiated per application types')
		user_title = _('Number of unique users initiating chats per application types')
		ratio_title = _('Ratio of chats initiated over unique user per application types')
		event_type = 'chats_initiated'
		event_y_axis_field = 'number_of_chats_initiated'
		event_y_axis_label = _('Number of chats initiated')

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
											  event_type)
		return plots

	def analyze_number_of_users_join_chats_per_date(self, 
													period_breaks='1 day', 
													minor_period_breaks=None,
													theme_seaborn_=True):

		cjt = self.cjt
		if cjt is None:
			return ()
		if cjt.dataframe.empty:
			return ()

		df = self.cjt.analyze_number_of_users_join_chats_per_date()
		if df is None:
			return ()
		plot_average_number_of_users_chatting_each_date = line_plot_x_axis_date(
															  df = df,
															  x_axis_field = 'timestamp_period',
															  y_axis_field = 'average_number_of_users_join_chats',
															  x_axis_label = 'Date',
															  y_axis_label = 'Average number of users',
															  title = 'Average number of users join chats',
															  period_breaks = period_breaks,
															  minor_breaks= minor_period_breaks,
															  theme_seaborn_=theme_seaborn_,
															  plot_name='average_number_user_join_chats')

		plot_total_number_of_users_chatting_each_date = line_plot_x_axis_date(
															  df = df,
															  x_axis_field = 'timestamp_period',
															  y_axis_field = 'total_number_of_users_join_chats',
															  x_axis_label = 'Date',
															  y_axis_label = 'Total number of users',
															  title = 'Total number of users join chats',
															  period_breaks = period_breaks,
															  minor_breaks= minor_period_breaks,
															  theme_seaborn_=theme_seaborn_,
															  plot_name='total_number_user_join_chats')

		plot_number_of_chats_created = line_plot_x_axis_date(
															  df = df,
															  x_axis_field = 'timestamp_period',
															  y_axis_field = 'number_of_chats_created',
															  x_axis_label = 'Date',
															  y_axis_label = 'Number of chats created',
															  title = 'Number of chats created',
															  period_breaks = period_breaks,
															  minor_breaks= minor_period_breaks,
															  theme_seaborn_=theme_seaborn_,
															  plot_name='chats_created')
		
		return (plot_average_number_of_users_chatting_each_date, 
				plot_total_number_of_users_chatting_each_date,
				plot_number_of_chats_created)

		

	