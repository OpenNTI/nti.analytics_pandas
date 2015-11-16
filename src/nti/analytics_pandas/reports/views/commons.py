#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from ...utils import Plot
from ...utils import save_plot_

def build_plot_images_dictionary_(plots, image_type='png'):
	images = {}
	for plot in plots:
		if isinstance(plot, Plot):
			image = save_plot_(plot.plot, plot.plot_name, image_type)
			images[plot.plot_name] = image
	return images
