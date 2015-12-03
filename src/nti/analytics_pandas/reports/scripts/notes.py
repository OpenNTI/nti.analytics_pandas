#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: notes.py 77907 2015-11-30 16:28:37Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from ..report import _configure_config
from ..report import _setup_configs
from ..report import process_args
from ..report import Report

from ..views import NoteEventsTimeseriesContext
from ..views import NoteEventsTimeseriesReportView

def main():
	# Parse command line args
	args = process_args()

	_setup_configs()

	_configure_config()
	
	# Create the output directory if it does not exist
	if not os.path.exists(args['output']):
		os.mkdir(args['output'])

	filepath = '%s/notes.pdf' %(args['output'])
	
	report_generator = Report(Context = NoteEventsTimeseriesContext, 
							  View = NoteEventsTimeseriesReportView, 
							  start_date = args['start_date'], 
							  end_date = args['end_date'], 
							  courses = args['courses'],
						 	  period_breaks = args['period_breaks'], 
						 	  minor_period_breaks = args['minor_period_breaks'],
						 	  theme_seaborn_ = args['theme_seaborn'], 
						 	  filepath=filepath)
	report = report_generator.build()

if __name__ == '__main__':  # pragma: no cover
	main()
