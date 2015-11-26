#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import atexit
import shutil
import tempfile
from collections import Mapping

import matplotlib.pyplot as plt

from z3c.rml import rml2pdf

from ...queries import QueryCourses

from ...utils import Plot
from ...utils import save_plot_

def build_images_dict_from_plot_dict(plots, image_type='png', dirname=None):
	"""
	proceed set of plots stored in dictionary
	"""
	images = {}
	if dirname is None:
		dirname = tempfile.mkdtemp()
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		atexit.register(shutil.rmtree, dirname)

	if isinstance(plots, Mapping):
		for key in plots:
			if isinstance(plots[key], Mapping):
				images[key] = build_images_dict_from_plot_dict(plots[key],
															   dirname=dirname,
															   image_type=image_type)
			elif isinstance(plots[key], (list, tuple)):
				images[key] = build_plot_images_dictionary(plots[key],
														   dirname=dirname,
														   image_type=image_type)
			elif isinstance(plots[key], Plot):
				images[key] = copy_plot_to_temporary_file(plots[key],
														  image_type=image_type)
	return images

def build_plot_images_dictionary(plots, image_type='png', dirname=None):
	images = {}
	for plot in plots:
		if isinstance(plot, Plot):
			filename = copy_plot_to_temporary_file(plot, image_type, dirname=dirname)
			images[plot.plot_name] = filename
	return images

def copy_plot_to_temporary_file_(plot, image_type, dirname=None):
	"""
	ega: please keep this function for further reference
	"""
	image = save_plot_(plot.plot, plot.plot_name, image_type)
	try:
		image_file = tempfile.NamedTemporaryFile(delete=False, dir=dirname)
		image.data.seek(0)
		shutil.copyfileobj(image.data, image_file)
	finally:
		image.data.close()
	return image_file.name

def copy_plot_to_temporary_file(plot, image_type, dirname=None):
	image_file = tempfile.NamedTemporaryFile(delete=False, dir=dirname)
	plt.figure.Figure = plot.plot.draw()
	plt.savefig(image_file.name, format=image_type)
	plt.close()
	return image_file.name

def get_course_names(session, courses_id):
	qc = QueryCourses(session)
	df = qc.get_context_name(courses_id)
	course_names = df['context_name'].tolist()
	return course_names

def create_pdf_file_from_rml(rml, filepath):
	pdf_stream = rml2pdf.parseString(rml)
	try:
		pdf_stream.seek(0)
		with open(filepath, 'w') as fp:
			shutil.copyfileobj(pdf_stream, fp)
	finally:
		pdf_stream.close()
