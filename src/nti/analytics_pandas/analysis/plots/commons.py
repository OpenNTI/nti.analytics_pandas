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
from ggplot import ylim
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_line
from ggplot import geom_point
from ggplot import facet_wrap
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import geom_histogram
from ggplot import scale_x_discrete

DATE_FORMAT = "%y-%m-%d"

def line_plot_x_axis_date(df,
						  x_axis_field,
						  y_axis_field,
						  x_axis_label,
						  y_axis_label,
						  title,
						  period_breaks,
						  minor_breaks=None):

	y_max = pd.Series.max(df[y_axis_field]) + 1
	line_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
		geom_line() + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if minor_breaks is not None:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 minor_breaks=minor_breaks,
											 labels=date_format(DATE_FORMAT))
	else:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 labels=date_format(DATE_FORMAT))
	return line_plot

def group_line_plot_x_axis_date(df,
								x_axis_field,
								y_axis_field,
								x_axis_label,
								y_axis_label,
								title,
								period_breaks, group_by,
								minor_breaks=None):

	y_max = pd.Series.max(df[y_axis_field]) + 1
	line_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field, color=group_by)) + \
		geom_line() + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if minor_breaks is not None:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 minor_breaks=minor_breaks,
											 labels=date_format(DATE_FORMAT))
	else:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 labels=date_format(DATE_FORMAT))

	return line_plot

def facet_line_plot_x_axis_date(df,
								x_axis_field,
								y_axis_field,
								x_axis_label,
								y_axis_label,
								title,
								period_breaks,
								group_by,
								facet,
								minor_breaks=None,
								scales='free',
								text_size=8):
	line_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field, color=group_by)) + \
		geom_line() + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=text_size, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		facet_wrap(facet, scales=scales)

	if minor_breaks is not None:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 minor_breaks=minor_breaks,
											 labels=date_format(DATE_FORMAT))
	else:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 labels=date_format(DATE_FORMAT))
	return line_plot

def histogram_plot(df,
				   x_axis_field,
				   y_axis_field,
				   x_axis_label, 
				   y_axis_label,
				   title,
				   stat):
	hist_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
				geom_histogram(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold")) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label))
	return hist_plot

def histogram_plot_x_axis_discrete(df, 
								   x_axis_field,
								   y_axis_field,
								   x_axis_label,
								   y_axis_label,
								   title, 
								   stat):
	hist_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
				geom_histogram(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold")) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label)) + \
				scale_x_discrete(x_axis_field)
	return hist_plot
