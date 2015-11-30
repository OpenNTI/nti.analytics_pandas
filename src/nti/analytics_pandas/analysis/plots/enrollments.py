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

from ggplot import aes
from ggplot import xlab
from ggplot import ylab
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_line
from ggplot import geom_point
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date

from .commons import generate_three_plots
from .commons import generate_three_group_by_plots
from .commons import group_line_plot_x_axis_date

class CourseCatalogViewsTimeseriesPlot(object):

	def __init__(self, ccvt):
		"""
		ccvt = CourseCatalogViewsTimeseries
		"""
		self.ccvt = ccvt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		return scatter plots of course catalog views during period of time
		it consists of:
			- number of course catalog views
			- number of unique users
			- ratio of course catalog views over unique users
		"""
		ccvt = self.ccvt
		df = ccvt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		event_title = _('Course catalog views during time period')
		user_title = _('Number of unique users viewing course catalog')
		ratio_title = _('Ratio of course catalog views over unique user')
		event_type = 'course_catalog_views'
		event_y_axis_field = 'number_of_course_catalog_views'
		event_y_axis_label = 'Number of course catalog views'
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

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		plot course catalog views based on user agent (device type)
		the plots consists of:
		- average time length users spent on viewing course catalog during time period
		- number of unique users during time period for each type of user agent
		"""
		ccvt = self.ccvt
		df = ccvt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of course catalog views per device_type')
		user_title = _('Number of unique users viewing course catalog per device_type')
		ratio_title = _('Ratio of course catalog views over unique user per device_type')
		event_type = 'course_catalog_views'
		event_y_axis_field = 'number_of_course_catalog_views'
		event_y_axis_label = 'Number of course catalog views'
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

class CourseEnrollmentsTimeseriesPlot(object):

	def __init__(self, cet):
		"""
		cevt = CourseEnrollmentsTimeseries
		"""
		self.cet = cet

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of course enrollments during period of time
		"""
		cet = self.cet
		df = cet.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_enrollments = \
				ggplot(df, aes(x='timestamp_period', y='number_of_enrollments')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(('Number of enrollments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of enrollments')) + \
				xlab(_('Date'))

		return (plot_course_enrollments,)

	def analyze_device_enrollment_types(self, period_breaks='1 month', minor_period_breaks='1 week'):
		"""
		return plots of the course enrollments grouped by user agent (device_type) and enrollment type
		"""
		cet = self.cet
		df = cet.analyze_device_enrollment_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df.rename(columns={	'type_name':'enrollment_type'}, inplace=True)

		plot_course_enrollments_by_device = \
				ggplot(df, aes(x='timestamp_period', y='number_of_enrollments', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of enrollments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of enrollments')) + \
				xlab(_('Date'))

		plot_course_enrollments_by_type = \
				ggplot(df, aes(x='timestamp_period', y='number_of_enrollments', color='enrollment_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of enrollments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of enrollments')) + \
				xlab(_('Date'))

		return (plot_course_enrollments_by_device, plot_course_enrollments_by_type)

class CourseDropsTimeseriesPlot(object):

	def __init__(self, cdt):
		"""
		cdvt = CourseDropsTimeseries
		"""
		self.cdt = cdt

	def explore_events(self, period_breaks='1 month', minor_period_breaks='1 week'):
		"""
		return scatter plots of course enrollments during period of time
		"""
		cdt = self.cdt
		df = cdt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_drops = \
				ggplot(df, aes(x='timestamp_period', y='number_of_course_drops')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of course drops during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of drops')) + \
				xlab(_('Date'))

		return (plot_course_drops,)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return plots of the course drops grouped by user agent (device_type)
		"""
		cdt = self.cdt
		df = cdt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_drops_by_device = \
				ggplot(df, aes(x='timestamp_period', y='number_of_course_drops', color='device_type')) + \
				geom_point() + \
				ggtitle(_('Number of course drops grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course drops')) + \
				xlab(_('Date'))

		return (plot_course_drops_by_device,)

	def analyze_enrollment_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return plots of the course drops grouped by enrollment types
		"""
		cdt = self.cdt
		df = cdt.analyze_enrollment_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		df.rename(columns={	'type_name':'enrollment_type'}, inplace=True)

		plot_course_drops_by_enrollment_type = \
				ggplot(df, aes(x='timestamp_period', y='number_of_course_drops', color='enrollment_type')) + \
				geom_point() + \
				ggtitle(_('Number of course drops grouped by enrollment types during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course drops')) + \
				xlab(_('Date'))

		return (plot_course_drops_by_enrollment_type,)

class CourseEnrollmentsEventsTimeseriesPlot(object):

	def __init__(self, ceet):
		"""
		ceet = CourseEnrollmentsEventsTimeseries
		"""
		self.ceet = ceet

	def explore_course_enrollments_vs_drops(self, period_breaks='1 week', minor_period_breaks='1 day'):
		ceet = self.ceet
		df = ceet.explore_course_enrollments_vs_drops()
		if len(df.index) <= 0:
			return ()

		plot_enrollments_events = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='total_events',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of events'),
										title=_('Number of course enrollments vs drops during period of time'),
										period_breaks=period_breaks,
										group_by='event_type',
										minor_breaks=minor_period_breaks)

		return (plot_enrollments_events)

	def explore_course_catalog_views_vs_enrollments(self, period_breaks='1 week', minor_period_breaks='1 day'):
		ceet = self.ceet
		df = ceet.explore_course_catalog_views_vs_enrollments()
		if len(df.index) <= 0:
			return ()

		plot_enrollments_events = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='total_events',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of events'),
									title=_('Number of course catalog views vs enrollments during period of time'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks)

		return (plot_enrollments_events,)
