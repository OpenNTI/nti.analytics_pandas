#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

import numpy as np

from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete

class NotesEventsTimeseriesPlot(object):

	def __init__(self, net):
		"""
		net = NotesEventsTimeseries
		"""
		self.net = net

	def explore_all_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		net = self.net
		df = net.combine_all_events()
		if len(df.index) <= 0:
			return ()

		plot_notes_events = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='total_events',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of notes events'),
								title=_('Number of notes events grouped by event type during period of time'),
								period_breaks=period_breaks,
								group_by='event_type',
								minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=_('Number of unique users creating notes events during period of time'),
								period_breaks=period_breaks,
								group_by='event_type',
								minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=_('Ratio of notes events over unique user on each available date'),
								period_breaks=period_breaks,
								group_by='event_type',
								minor_breaks=minor_period_breaks)

		return (plot_notes_events, plot_unique_users, plot_ratio)

class NotesCreationTimeseriesPlot(object):

	def __init__(self, nct):
		"""
		nct = NotesCreationTimeseries
		"""
		self.nct = nct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of notes created')
		user_title = _('Number of unique users creating notes')
		ratio_title = _('Ratio of notes created over unique user')

		plots = self.generate_plots(df, event_title, user_title,
									ratio_title, period_breaks, minor_period_breaks)

		return (plots)

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of notes created per course sections')
			user_title = _('Number of unique users creating notes per course sections')
			ratio_title = _('Ratio of notes created over unique user per course sections')
			all_section_plots = self.generate_group_by_plot(df,
															group_by,
															event_title,
															user_title,
															ratio_title,
															period_breaks,
															minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of notes created in %s' % (context_name)
			user_title = 'Number of unique users creating notes in %s' % (context_name)
			ratio_title = 'Ratio of notes created over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks,
												minor_period_breaks)
			plots.append(section_plots)

		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
					   period_breaks='1 week', minor_period_breaks='1 day'):

		plot_notes_created = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_notes_created',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of notes created'),
								title=event_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=user_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		return (plot_notes_created, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		dataframe = nct.dataframe
		df = nct.analyze_device_types(dataframe)

		group_by = 'device_type'
		event_title = _('Number of notes created grouped by device types')
		user_title = _('Number of unique users creating notes grouped by device types')
		ratio_title = _('Ratio of notes created grouped by device types over unique user')
		device_plots = self.generate_group_by_plot(df,
												   group_by,
												   event_title,
												   user_title,
												   ratio_title,
												   period_breaks,
												   minor_period_breaks)
		return (device_plots,)

	def analyze_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		df = nct.analyze_resource_types()

		event_title = _('Number of notes created grouped by resource types')
		user_title = _('Number of unique users creating notes grouped by resource types')
		ratio_title = _('Ratio of notes created grouped by resource types over unique user')
		group_by = 'resource_type'
		resource_plots = self.generate_group_by_plot(df,
													 group_by,
													 event_title,
													 user_title,
													 ratio_title,
													 period_breaks,
													 minor_period_breaks)

		return (resource_plots,)

	def plot_the_most_active_users(self, max_rank_number=10):
		nct = self.nct
		users_df = nct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
								df=users_df,
								x_axis_field='username' ,
								y_axis_field='number_of_notes_created',
								x_axis_label=_('Username'),
								y_axis_label=_('Number of notes created'),
								title=_('The most active users creating notes'),
								stat='identity')

		return (plot_users,)

	def analyze_sharing_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		dataframe = nct.dataframe
		df = nct.analyze_sharing_types(dataframe)

		event_title = _('Number of notes created grouped by sharing types')
		user_title = _('Number of unique users creating notes grouped by sharing types')
		ratio_title = _('Ratio of notes created grouped by sharing types over unique user')

		group_by = 'sharing'
		sharing_plots = self.generate_group_by_plot(df,
													group_by,
													event_title,
													user_title,
													ratio_title,
													period_breaks,
													minor_period_breaks)

		return (sharing_plots,)

	def generate_group_by_plot(self, df, group_by, event_title, user_title, ratio_title,
							   period_breaks='1 week', minor_period_breaks='1 day'):
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_notes_created = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_notes_created',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of notes created'),
								title=event_title,
								period_breaks=period_breaks,
								group_by=group_by,
								minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=user_title,
								period_breaks=period_breaks,
								group_by=group_by,
								minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								group_by=group_by,
								minor_breaks=minor_period_breaks)

		return (plot_notes_created, plot_unique_users, plot_ratio)

	def analyze_notes_created_on_videos(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nct = self.nct
		(sharing_df, device_df) = nct.analyze_notes_created_on_videos()

		# generate sharing types plots
		group_by = 'sharing'
		event_title = _('Number of notes created on videos grouped by sharing types')
		user_title = _('Number of unique users creating notes on videos grouped by sharing types')
		ratio_title = _('Ratio of notes created on videos grouped by sharing types over unique user')
		sharing_plots = self.generate_group_by_plot(sharing_df,
													group_by,
													event_title,
													user_title,
													ratio_title,
													period_breaks,
													minor_period_breaks)

		# generate device types plots
		group_by = 'device_type'
		event_title = _('Number of notes created on videos grouped by device types')
		user_title = _('Number of unique users creating notes on videos grouped by device types')
		ratio_title = _('Ratio of notes created on videos grouped by device types over unique user')
		device_plots = self.generate_group_by_plot(device_df,
												   group_by,
												   event_title,
												   user_title,
												   ratio_title,
												   period_breaks,
												   minor_period_breaks)
		return (sharing_plots, device_plots)

class NotesViewTimeseriesPlot(object):

	def __init__(self, nvt):
		"""
		nvt = NotesViewTimeseries
		"""
		self.nvt = nvt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of notes viewed during period of time')
		user_title = _('Number of unique users viewing notes during period of time')
		ratio_title = _('Ratio of notes viewed over unique user on each available date')

		plots = self.generate_plots(df, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks)
		return (plots)

	def analyze_total_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of notes viewed per course sections')
			user_title = _('Number of unique users viewing notes per course sections')
			ratio_title = _('Ratio of notes viewed over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of notes viewed in %s' % (context_name)
			user_title = 'Number of unique users viewing notes in %s' % (context_name)
			ratio_title = 'Ratio of notes viewed over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks, minor_period_breaks)
			plots.append(section_plots)

		return plots

	def generate_plots(self, df, event_title, user_title,
						ratio_title, period_breaks, minor_period_breaks):

		plot_notes_viewed = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_note_views',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of note views'),
								title=event_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=user_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks)

		return (plot_notes_viewed, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
							   period_breaks='1 week', minor_period_breaks='1 day'):

		plot_notes_viewed = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_note_views',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of note views'),
								title=event_title,
								period_breaks=period_breaks,
								group_by=group_by,
								minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='number_of_unique_users',
								x_axis_label=_('Date'),
								y_axis_label=_('Number of unique users'),
								title=user_title,
								period_breaks=period_breaks,
								group_by=group_by,
								minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								group_by=group_by,
								minor_breaks=minor_period_breaks)

		return (plot_notes_viewed, plot_unique_users, plot_ratio)

	def analyze_total_events_based_on_sharing_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_sharing_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'sharing'
		event_title = _('Number of notes viewed grouped by sharing types')
		user_title = _('Number of unique users viewing notes grouped by sharing types')
		ratio_title = _('Ratio of notes viewed grouped by sharing types over unique user')

		plots = self.generate_group_by_plots(df, group_by, event_title, user_title,
											ratio_title, period_breaks, minor_period_breaks)

		return plots

	def plot_the_most_active_users(self, max_rank_number=10):
		nvt = self.nvt
		users_df = nvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(df=users_df,
													x_axis_field='username' ,
													y_axis_field='number_of_note_views',
													x_axis_label=_('Username'),
													y_axis_label=_('Number of notes viewed'),
													title=_('The most active users viewing notes'),
													stat='identity')
		return (plot_users,)

	def analyze_total_events_based_on_device_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_device_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of notes viewed grouped by device types')
		user_title = _('Number of unique users viewing notes grouped by device types')
		ratio_title = _('Ratio of notes viewed grouped by device types over unique user')

		plots = self.generate_group_by_plots(df, group_by, event_title, user_title,
											ratio_title, period_breaks, minor_period_breaks)

		return (plots)

	def analyze_total_events_based_on_resource_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'resource_type'
		event_title = _('Number of notes viewed grouped by resource types')
		user_title = _('Number of unique users viewing notes grouped by resource types')
		ratio_title = _('Ratio of notes viewed grouped by resource types over unique user')

		plots = self.generate_group_by_plots(df, group_by, event_title, user_title,
											 ratio_title, period_breaks,
											 minor_period_breaks)

		return (plots)

	def analyze_unique_events_based_on_sharing_type(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nvt = self.nvt
		df = nvt.analyze_unique_events_based_on_sharing_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		title = _('Number of notes viewed grouped by sharing types during period of time')
		plot_unique_notes_viewed = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_notes_viewed',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of notes viewed'),
										title=title,
										period_breaks=period_breaks,
										group_by='sharing',
										minor_breaks=minor_period_breaks)

		return (plot_unique_notes_viewed,)

class NoteLikesTimeseriesPlot(object):

	def __init__(self, nlt):
		"""
		nlt = NoteLikesTimeseries
		"""
		self.nlt = nlt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nlt = self.nlt
		df = nlt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of note likes during period of time')
		user_title = _('Number of unique users liking notes during period of time')
		ratio_title = _('Ratio of note likes over unique user on each available date')
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nlt = self.nlt
		df = nlt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of note likes per course sections')
			user_title = _('Number of unique users liking notes per course sections')
			ratio_title = _('Ratio of note likes over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of note likes in %s' % (context_name)
			user_title = 'Number of unique users liking notes in %s' % (context_name)
			ratio_title = 'Ratio of note likes over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks, minor_period_breaks)
			plots.append(section_plots)

		return plots

	def analyze_events_per_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nlt = self.nlt
		df = nlt.analyze_events_per_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of note likes grouped by device types')
		user_title = _('Number of unique users liking notes grouped by device types')
		ratio_title = _('Ratio of note likes over unique user grouped by device types')
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks)
		return plots

	def analyze_events_per_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nlt = self.nlt
		df = nlt.analyze_events_per_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'resource_type'
		event_title = _('Number of note likes grouped by resource types')
		user_title = _('Number of unique users liking notes grouped by resource types')
		ratio_title = _('Ratio of note likes over unique user grouped by resource types')
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks)
		return plots

	def generate_plots(self, df, event_title, user_title,
						ratio_title, period_breaks, minor_period_breaks):
		plot_note_likes = line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_note_likes',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of note likes'),
							title=event_title,
							period_breaks=period_breaks,
							minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_unique_users',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of unique users'),
							title=user_title,
							period_breaks=period_breaks,
							minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='ratio',
							x_axis_label=_('Date'),
							y_axis_label=_('Ratio'),
							title=ratio_title,
							period_breaks=period_breaks,
							minor_breaks=minor_period_breaks)

		return (plot_note_likes, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks):

		plot_note_likes = group_line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_note_likes',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of note likes'),
							title=event_title,
							period_breaks=period_breaks,
							group_by=group_by,
							minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_unique_users',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of unique users'),
							title=user_title,
							period_breaks=period_breaks,
							group_by=group_by,
							minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='ratio',
							x_axis_label=_('Date'),
							y_axis_label=_('Ratio'),
							title=ratio_title,
							period_breaks=period_breaks,
							group_by=group_by,
							minor_breaks=minor_period_breaks)

		return (plot_note_likes, plot_unique_users, plot_ratio)

class NoteFavoritesTimeseriesPlot(object):

	def __init__(self, nft):
		"""
		nft = NoteFavoritesTimeseries
		"""
		self.nft = nft

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nft = self.nft
		df = nft.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of note favorites during period of time')
		user_title = _('Number of unique users voting notes as favorite during period of time')
		ratio_title = _('Ratio of note favorites over unique user on each available date')
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nft = self.nft
		df = nft.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of note favorites per course sections')
			user_title = _('Number of unique users voting notes as favorites per course sections')
			ratio_title = _('Ratio of note favorites over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of note favorites in %s' % (context_name)
			user_title = 'Number of unique users voting notes as favorites in %s' % (context_name)
			ratio_title = 'Ratio of note favorites over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df, event_title, user_title,
												ratio_title, period_breaks, minor_period_breaks)
			plots.append(section_plots)

		return plots

	def analyze_events_per_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nft = self.nft
		df = nft.analyze_events_per_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of note favorites grouped by device types')
		user_title = _('Number of unique users voting notes as favorite grouped by device types')
		ratio_title = _('Ratio of note favorites over unique user grouped by device types')
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks)
		return plots

	def analyze_events_per_resource_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		nft = self.nft
		df = nft.analyze_events_per_resource_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'resource_type'
		event_title = _('Number of note favorites grouped by resource types')
		user_title = _('Number of unique users voting notes as favorite grouped by resource types')
		ratio_title = _('Ratio of note favorites over unique user grouped by resource types')
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks)

		return plots

	def generate_plots(self, df, event_title, user_title,
						ratio_title, period_breaks, minor_period_breaks):

		plot_note_favorites = line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_note_favorites',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of note favorites'),
							title=event_title,
							period_breaks=period_breaks,
							minor_breaks=minor_period_breaks)

		plot_unique_users = line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_unique_users',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of unique users'),
							title=user_title,
							period_breaks=period_breaks,
							minor_breaks=minor_period_breaks)

		plot_ratio = line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='ratio',
							x_axis_label=_('Date'),
							y_axis_label=_('Ratio'),
							title=ratio_title,
							period_breaks=period_breaks,
							minor_breaks=minor_period_breaks)

		return (plot_note_favorites, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
						event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks):
		plot_note_favorites = group_line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_note_favorites',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of note favorites'),
							title=event_title,
							period_breaks=period_breaks,
							group_by=group_by,
							minor_breaks=minor_period_breaks)

		plot_unique_users = group_line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='number_of_unique_users',
							x_axis_label=_('Date'),
							y_axis_label=_('Number of unique users'),
							title=user_title,
							period_breaks=period_breaks,
							group_by=group_by,
							minor_breaks=minor_period_breaks)

		plot_ratio = group_line_plot_x_axis_date(
							df=df,
							x_axis_field='timestamp_period',
							y_axis_field='ratio',
							x_axis_label=_('Date'),
							y_axis_label=_('Ratio'),
							title=ratio_title,
							period_breaks=period_breaks,
							group_by=group_by,
							minor_breaks=minor_period_breaks)

		return (plot_note_favorites, plot_unique_users, plot_ratio)
