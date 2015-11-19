#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from collections import Mapping

from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from ...queries import QueryCourses

from ...utils import Plot
from ...utils import save_plot_

def build_images_dict_from_plot_dict(plots, image_type='png'):
	"""
	proceed set of plots stored in dictionary
	"""
	images = {}
	if isinstance(plots, Mapping):
		for key in plots:
			if isinstance(plots[key], Mapping):
				images[key] = build_images_dict_from_plot_dict(plots[key])
			elif isinstance(plots[key], (list,tuple)):
				images[key] = build_plot_images_dictionary(plots[key])
			elif isinstance(plots[key], Plot):
				images[key] = copy_plot_to_temporary_file(plots[key], image_type)
	return images

def build_plot_images_dictionary(plots, image_type='png'):
	images = {}
	for plot in plots:
		if isinstance(plot, Plot):
			filename = copy_plot_to_temporary_file(plot, image_type)
			images[plot.plot_name] = filename
	return images

def copy_plot_to_temporary_file(plot, image_type, dirname=None):
	# TODO: delete the named temporary files after using it to generate report
	image = save_plot_(plot.plot, plot.plot_name, image_type)
	image_file = NamedTemporaryFile(delete=False, dir=dirname)
	image.data.seek(0)
	copyfileobj(image.data, image_file)
	image.data.close()
	return image_file.name

def get_course_names(session, courses_id):
	qc = QueryCourses(session)
	df = qc.get_context_name(courses_id)
	course_names = df['context_name'].tolist()
	return course_names
