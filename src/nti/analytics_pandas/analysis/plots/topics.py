#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory as _

import pandas as pd

import numpy as np

from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import histogram_plot_x_axis_discrete

class TopicsEventsTimeseriesPlot(object):

	def __init__(self, tet):
		"""
		tet = TopicsEventsTimeseries
		"""
		self.tet = tet

	def explore_all_events(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):
		tet = self.tet
		df = tet.combine_all_events_per_date()
		if len(df.index) <= 0:
			return ()

		plot_topics_events = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='total_events',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of topics events'),
									title=_('Number of topics events grouped by event type during period of time'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_unique_users = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='total_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=_('Number of unique users creating topics events during period of time'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=_('Ratio of topics events over unique user on each available date'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		return (plot_topics_events, plot_unique_users, plot_ratio)

class TopicsCreationTimeseriesPlot(object):

	def __init__(self, tct):
		"""
		tct = TopicsCreationTimeseries
		"""
		self.tct = tct

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		"""
		return plots of topics created during period of time
		it consists of:
			- number of topics created
			- number of unique users
			- ratio of topics created over unique users
		"""
		tct = self.tct
		df = tct.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topics created during period of time')
		user_title = _('Number of unique users creating topics during period of time')
		ratio_title = _('Ratio of topics created over unique user on each available date')
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day',
											theme_seaborn_=True):
		tct = self.tct
		df = tct.analyze_events_per_course_sections()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topics created per course sections')
			user_title = _('Number of unique users creating topics per course sections')
			ratio_title = _('Ratio of topics created over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of topics created in %s' % (context_name)
			user_title = 'Number of unique users creating topics in %s' % (context_name)
			ratio_title = 'Ratio of topics created over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_)
			plots.append(section_plots)

		return plots

	def analyze_events_per_device_types(self, period_breaks='1 week', minor_period_breaks='1 day',
										theme_seaborn_=True):
		tct = self.tct
		df = tct.analyze_events_per_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of topics created per device types')
		user_title = _('Number of unique users creating topics per device types')
		ratio_title = _('Ratio of topics created over unique user per device types')
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks, theme_seaborn_):

		plot_topics_created = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_topics_created',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of topics created'),
									title=event_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_unique_users = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_)

		return (plot_topics_created, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
						event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks, theme_seaborn_):

		plot_topics_created = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_topics_created',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of topics created'),
										title=event_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_)

		plot_unique_users = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_users',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of unique users'),
										title=user_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		return (plot_topics_created, plot_unique_users, plot_ratio)

class TopicViewsTimeseriesPlot(object):

	def __init__(self, tvt):
		"""
		tvt = TopicViewsTimeseries
		"""
		self.tvt = tvt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		"""
		return plots of topics viewed during period of time
		it consists of:
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topics viewed during period of time')
		user_title = _('Number of unique users viewing topics during period of time')
		ratio_title = _('Ratio of topics viewed over unique user on each available date')
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day',
											theme_seaborn_=True):
		tvt = self.tvt
		df = tvt.analyze_events_per_course_sections()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topics viewed per course sections')
			user_title = _('Number of unique users viewing topics per course sections')
			ratio_title = _('Ratio of topics viewed over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of topics viewed in %s' % (context_name)
			user_title = 'Number of unique users viewing topics in %s' % (context_name)
			ratio_title = 'Ratio of topics viewed over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_)
			plots.append(section_plots)
		return plots

	def analyze_device_types(self, period_breaks='1 day', minor_period_breaks=None,
							theme_seaborn_=True):
		"""
		return plots of topics viewed grouped by device type during period of time
		it consists of:
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of topics viewed grouped by device types')
		user_title = _('Number of unique users viewing topics grouped by device types')
		ratio_title = _('Ratio of topics viewed over unique user grouped by device types')
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks, theme_seaborn_):

		plot_topics_viewed = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_topics_viewed',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of topics viewed'),
									title=event_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_unique_users = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_)

		return (plot_topics_viewed, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
								event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks,
								theme_seaborn_):

		plot_topics_viewed = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_topics_viewed',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of topics viewed'),
										title=event_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_)

		plot_unique_users = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_users',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of unique users'),
										title=user_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		return (plot_topics_viewed, plot_unique_users, plot_ratio)

	def plot_the_most_active_users(self, max_rank_number=10):
		tvt = self.tvt
		users_df = tvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
									df=users_df,
									x_axis_field='username' ,
									y_axis_field='number_of_topics_viewed',
									x_axis_label=_('Username'),
									y_axis_label=_('Number of topics viewed'),
									title=_('The most active users viewing topics'),
									stat='identity')

		return (plot_users,)

class TopicLikesTimeseriesPlot(object):

	def __init__(self, tlt):
		"""
		tlt = TopicLikesTimeseries
		"""
		self.tlt = tlt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		"""
		return plots of topic likes during period of time
		it consists of:
			- number of topic likes
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tlt = self.tlt
		df = tlt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topic likes during period of time')
		user_title = _('Number of unique users liking topics during period of time')
		ratio_title = _('Ratio of topic likes over unique user on each available date')
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day',
											theme_seaborn_=True):
		tlt = self.tlt
		df = tlt.analyze_events_per_course_sections()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topic likes per course sections')
			user_title = _('Number of unique users liking topics per course sections')
			ratio_title = _('Ratio of topic likes over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of topic likes in %s' % (context_name)
			user_title = 'Number of unique users liking topics in %s' % (context_name)
			ratio_title = 'Ratio of topic likes over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_)
			plots.append(section_plots)
		return plots

	def analyze_events_per_device_types(self, period_breaks='1 day', minor_period_breaks=None,
										theme_seaborn_=True):
		"""
		return plots of topic likes grouped by device  types
		it consists of:
			- number of topic likes
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tlt = self.tlt
		df = tlt.analyze_events_per_device_types(tlt.dataframe)
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of topics likes grouped by device types')
		user_title = _('Number of unique users liking topics grouped by device types')
		ratio_title = _('Ratio of topic likes over unique user grouped by device types')
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks, theme_seaborn_):

		plot_topic_likes = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_topic_likes',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of topic likes'),
									title=event_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_unique_users = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_)

		return (plot_topic_likes, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
								event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks,
								theme_seaborn_):

		plot_topic_likes = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_topic_likes',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of topic likes'),
									title=event_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_unique_users = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		return (plot_topic_likes, plot_unique_users, plot_ratio)

class TopicFavoritesTimeseriesPlot(object):

	def __init__(self, tft):
		"""
		tft = TopicFavoritesTimeseries
		"""
		self.tft = tft

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		"""
		return plots of topic favorites during period of time
		it consists of:
			- number of topic favorites
			- number of unique users
			- ratio of topic favorites over unique users
		"""
		tft = self.tft
		df = tft.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topic favorites during period of time')
		user_title = _('Number of unique users choosing topics as favorites during period of time')
		ratio_title = _('Ratio of topic favorites over unique user on each available date')
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week', minor_period_breaks='1 day',
											theme_seaborn_=True):
		tft = self.tft
		df = tft.analyze_events_per_course_sections()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topic favorites per course sections')
			user_title = _('Number of unique users choosing topics as favorite per course sections')
			ratio_title = _('Ratio of topic favorites over unique user per course sections')
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = 'Number of topic favorites in %s' % (context_name)
			user_title = 'Number of unique users choosing topics as favorites in %s' % (context_name)
			ratio_title = 'Ratio of topic favorites over unique user in %s' % (context_name)
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_)
			plots.append(section_plots)
		return plots

	def analyze_events_per_device_types(self, period_breaks='1 day', minor_period_breaks=None,
										theme_seaborn_=True):
		"""
		return plots of topic favorites grouped by device  types
		it consists of:
			- number of topic favorites
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tft = self.tft
		df = tft.analyze_events_per_device_types(tft.dataframe)
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of topics favorites grouped by device types')
		user_title = _('Number of unique users choosing topics as favorite grouped by device types')
		ratio_title = _('Ratio of topic favorites over unique user grouped by device types')
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
						period_breaks, minor_period_breaks, theme_seaborn_):

		plot_topic_favorites = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_topic_favorites',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of topic favorites'),
										title=event_title,
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_)

		plot_unique_users = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_users',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of unique users'),
										title=user_title,
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_)

		plot_ratio = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label=_('Date'),
								y_axis_label=_('Ratio'),
								title=ratio_title,
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_)

		return (plot_topic_favorites, plot_unique_users, plot_ratio)

	def generate_group_by_plots(self, df, group_by,
								event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks,
								theme_seaborn_):

		plot_topic_favorites = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_topic_favorites',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of topic favorites'),
											title=event_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_)

		plot_unique_users = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_users',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique users'),
											title=user_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_)

		plot_ratio = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									group_by=group_by,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_)

		return (plot_topic_favorites, plot_unique_users, plot_ratio)
