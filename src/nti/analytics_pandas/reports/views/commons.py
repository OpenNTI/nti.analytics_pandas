#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from ...queries import QueryCourses

from ...utils import Plot
from ...utils import save_plot_

def build_plot_images_dictionary_(plots, image_type='png'):
	# TODO: delete the named temporary files after using it to generate report
	images = {}
	for plot in plots:
		if isinstance(plot, Plot):
			image = save_plot_(plot.plot, plot.plot_name, image_type)
			image_file = NamedTemporaryFile(delete=False)
			image.data.seek(0)
			copyfileobj(image.data, image_file)
			image.data.close()
			images[plot.plot_name] = image_file.name
	return images

def get_course_names(session, courses_id):
	qc = QueryCourses(session)
	df = qc.get_context_name(courses_id)
	course_names = df['context_name'].tolist()
	return course_names