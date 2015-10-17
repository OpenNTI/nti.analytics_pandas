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

class CourseCatalogViewsTimeseriesPlot(object):

	def __init__(self, ccvt):
		"""
		ccvt = CourseCatalogViewsTimeseries
		"""
		self.ccvt = ccvt

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return scatter plots of course catalog views during period of time
		it consists of :
			- number of course catalog views
			- number of unique users
			- ratio of course catalog views over unique users
		"""
		ccvt = self.ccvt
		df = ccvt.explore_ratio_of_events_over_unique_users_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_catalog_views = \
				ggplot(df, aes(x='timestamp_period', y='total_course_catalog_views')) + \
				geom_line() + \
				geom_point(color='orange') + \
				ggtitle(_('Number of course catalog views during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course catalog views')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='total_unique_users')) + \
				geom_line() + \
				geom_point(color='blue') + \
				ggtitle(_('Number of unique users viewing course catalog during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		plot_ratio = \
				ggplot(df, aes(x='timestamp_period', y='ratio')) + \
				geom_line() + \
				geom_point(color='red') + \
				ggtitle(_('Ratio of course catalog views over unique user on each available date')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Ratio')) + \
				xlab(_('Date'))

		return (plot_catalog_views, plot_unique_users, plot_ratio)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		plot course catalog views based on user agent (device type)
		the plots consists of :
		- average time length users spent on viewing course catalog during time period
		- number of unique users during time period for each type of user agent
		"""
		ccvt = self.ccvt
		df = ccvt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_average_time_length = \
				ggplot(df, aes(x='timestamp_period', y='average_time_length', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Average time length user spent viewing course catalog during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Average time length (in seconds)')) + \
				xlab(_('Date'))

		plot_catalog_view_events = \
				ggplot(df, aes(x='timestamp_period', y='number_of_course_catalog_views', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of course catalog views during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of unique users')) + \
				xlab(_('Date'))

		plot_unique_users = \
				ggplot(df, aes(x='timestamp_period', y='number_of_unique_users', color='device_type')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of unique users viewing course catalog during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab('Number of unique users') + \
				xlab(_('Date'))

		return (plot_average_time_length, plot_catalog_view_events, plot_unique_users)

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
		df = cet.explore_number_of_events_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_enrollments = \
				ggplot(df, aes(x='timestamp_period', y='total_enrollments')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(('Number of enrollments during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of enrollments')) + \
				xlab(_('Date'))

		return (plot_course_enrollments)

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
		df = cdt.explore_number_of_events_based_timestamp_date()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_drops = \
				ggplot(df, aes(x='timestamp_period', y='total_drops')) + \
				geom_line() + \
				geom_point() + \
				ggtitle(_('Number of course drops during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of drops')) + \
				xlab(_('Date'))

		return (plot_course_drops)

	def analyze_device_enrollment_types(self, period_breaks='1 week', minor_period_breaks='1 day'):
		"""
		return plots of the course drops grouped by user agent (device_type) and enrollment type
		"""
		cdt = self.cdt
		df = cdt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		df.rename(columns={	'type_name':'enrollment_type'}, inplace=True)

		plot_course_drops_by_device = \
				ggplot(df, aes(x='timestamp_period', y='number_of_course_drops', color='device_type')) + \
				geom_point() + \
				ggtitle(_('Number of course drops grouped by device type during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course drops')) + \
				xlab(_('Date'))

		plot_course_drops_by_enrollment_type = \
				ggplot(df, aes(x='timestamp_period', y='number_of_course_drops', color='enrollment_type')) + \
				geom_point() + \
				ggtitle(_('Number of course drops grouped by enrollment types during period of time')) + \
				theme(title=element_text(size=10, face="bold")) + \
				scale_x_date(breaks=period_breaks, minor_breaks=minor_period_breaks, labels=date_format("%y-%m-%d")) + \
				ylab(_('Number of course drops')) + \
				xlab(_('Date'))

		return (plot_course_drops_by_device, plot_course_drops_by_enrollment_type)
