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
from ggplot import geom_bar
from ggplot import geom_line
from ggplot import geom_point
from ggplot import facet_wrap
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import theme_seaborn
from ggplot import geom_histogram
from ggplot import scale_x_discrete

from ...utils import Plot

DATE_FORMAT = "%Y-%m-%d"

def line_plot_x_axis_date(df,
						  x_axis_field,
						  y_axis_field,
						  x_axis_label,
						  y_axis_label,
						  title,
						  period_breaks,
						  minor_breaks=None,
						  theme_seaborn_=True,
						  plot_name=None):

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
	if theme_seaborn_:
		line_plot = line_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, line_plot)
		return plot

	return line_plot

def scatter_plot_x_axis_date(df,
						 	 x_axis_field,
						  	 y_axis_field,
						  	 x_axis_label,
						  	 y_axis_label,
						  	 title,
						  	 period_breaks,
						  	 minor_breaks=None,
						  	 theme_seaborn_=True,
						  	 plot_name=None):

	y_max = pd.Series.max(df[y_axis_field]) + 1
	scatter_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if minor_breaks is not None:
		scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											 	   minor_breaks=minor_breaks,
											 	   labels=date_format(DATE_FORMAT))
	else:
		scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											 	   labels=date_format(DATE_FORMAT))

	if theme_seaborn_:
		scatter_plot = scatter_plot + theme_seaborn()
	
	if plot_name is not None:
		plot = Plot.process(plot_name, scatter_plot)
		return plot

	return scatter_plot

def group_line_plot_x_axis_date(df,
								x_axis_field,
								y_axis_field,
								x_axis_label,
								y_axis_label,
								title,
								period_breaks,
								group_by,
								minor_breaks=None,
								theme_seaborn_=True,
								plot_name=None):

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
	if theme_seaborn_ :
		line_plot = line_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, line_plot)
		return plot

	return line_plot

def group_scatter_plot_x_axis_date(df,
								   x_axis_field,
								   y_axis_field,
								   x_axis_label,
								   y_axis_label,
								   title,
								   period_breaks,
								   group_by,
								   minor_breaks=None,
								   theme_seaborn_=True,
								   plot_name=None):

	y_max = pd.Series.max(df[y_axis_field]) + 1
	scatter_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field, color=group_by)) + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if minor_breaks is not None:
		scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											 	   minor_breaks=minor_breaks,
											 	   labels=date_format(DATE_FORMAT))
	else:
		scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											 	   labels=date_format(DATE_FORMAT))
	if theme_seaborn_:
		scatter_plot = scatter_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, scatter_plot)
		return plot

	return scatter_plot

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
				   stat,
				   plot_name=None):
	hist_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
				geom_histogram(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold")) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label))

	if plot_name is not None:
		plot = Plot.process(plot_name, hist_plot)
		return plot

	return hist_plot

def histogram_plot_x_axis_discrete(df,
								   x_axis_field,
								   y_axis_field,
								   x_axis_label,
								   y_axis_label,
								   title,
								   stat,
								   theme_seaborn_=True,
								   plot_name=None):
	hist_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
				geom_histogram(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold"),
					  axis_text_x=element_text(angle=15, hjust=1)) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label)) + \
				scale_x_discrete(x_axis_field)

	if plot_name is not None:
		plot = Plot.process(plot_name, hist_plot)
		return plot

	return hist_plot

def bar_plot_with_fill(df,
					   x_axis_field,
					   y_axis_field,
					   x_axis_label,
					   y_axis_label,
					   title,
					   stat,
					   fill,
					   theme_seaborn_=True,
					   plot_name=None):

	bar_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field, fill=fill)) + \
				geom_bar(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold"),
					  axis_text_x=element_text(angle=15, hjust=1)) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label))

	if plot_name is not None:
		plot = Plot.process(plot_name, bar_plot)
		return plot

	return bar_plot
