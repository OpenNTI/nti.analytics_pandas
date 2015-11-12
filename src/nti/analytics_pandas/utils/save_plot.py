#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from StringIO import StringIO

import matplotlib.pyplot as plt

class Image(object):

	@classmethod
	def process(cls, filename, data):
		me = cls()
		me.filename = filename
		me.data = data
		return me

class Plot(object):

	@classmethod
	def process(cls, plot_name, plot):
		me = cls()
		me.plot_name = plot_name
		me.plot = plot
		return me

def save_plot_to_png(plot, image_filename):
	plt.figure.Figure = plot.draw()
	buf = StringIO()
	plt.savefig(buf, format='png')
	plt.close()
	image = Image.process(image_filename, buf)
	return image
