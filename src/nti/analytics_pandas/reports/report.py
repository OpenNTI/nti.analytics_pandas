#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import logging
import argparse

from zope.configuration import xmlconfig, config

import nti.analytics_pandas

from ..databases import DBConnection

from .views import AssessmentsEventsTimeseriesContext
from .views import AssessmentsEventsTimeseriesReportView

from .views import BookmarksTimeseriesContext
from .views import BookmarksTimeseriesReportView

from .views import EnrollmentTimeseriesContext
from .views import EnrollmentTimeseriesReportView

from .views import create_pdf_file_from_rml
from .views import cleanup_temporary_file

from .views import ForumsTimeseriesContext
from .views import ForumsTimeseriesReportView

from .views import HighlightsTimeseriesContext
from .views import HighlightsTimeseriesReportView

from .views import NoteEventsTimeseriesContext
from .views import NoteEventsTimeseriesReportView

from .views import ResourceViewsTimeseriesContext
from .views import ResourceViewsTimeseriesReportView

from .views import TopicsTimeseriesContext
from .views import TopicsTimeseriesReportView

from .z3c_zpt import ViewPageTemplateFile

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser(description="NTI Analytics")
	arg_parser.add_argument('-o', '--output',
							 default='output',
							 help="The output directory. The default is: %s" % 'output')
	return arg_parser.parse_args()

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)

def _setup_configs():
	_configure_logging()

def std_report_layout_rml():
	path = os.path.join(os.path.dirname(__file__), 'templates/std_report_layout.rml')
	return path

def template(path):
	result = ViewPageTemplateFile(path,
								  auto_reload=(False,),
								  debug=False)
	return result

def build_rml(Context, View, session, start_date, end_date, courses,
			  period_breaks, minor_period_breaks, theme_seaborn_):

	context = Context(session, start_date, end_date, courses,
					  period_breaks, minor_period_breaks, theme_seaborn_)
	view = View(context)
	view()
	path = std_report_layout_rml()
	system = {'view':view, 'context':context}
	rml = template(path).bind(view)(**system)
	data = view.options['data']
	return rml, data

def generate_assessments_report(session, start_date, end_date, courses,
			  					period_breaks, minor_period_breaks, theme_seaborn_,
			  					output_dir):
	Context = AssessmentsEventsTimeseriesContext
	View = AssessmentsEventsTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/assessments.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def generate_bookmarks_report(session, start_date, end_date, courses,
			  					period_breaks, minor_period_breaks, theme_seaborn_,
			  					output_dir):
	Context = BookmarksTimeseriesContext
	View = BookmarksTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/bookmarks.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report


def generate_enrollments_report(session, start_date, end_date, courses,
			  					period_breaks, minor_period_breaks, theme_seaborn_,
			  					output_dir):
	Context = EnrollmentTimeseriesContext
	View = EnrollmentTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/enrollments.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def generate_forums_report(session, start_date, end_date, courses,
			  			   period_breaks, minor_period_breaks, theme_seaborn_,
			  			   output_dir):
	Context = ForumsTimeseriesContext
	View = ForumsTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/forums.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def generate_highlights_report(session, start_date, end_date, courses,
				  			   period_breaks, minor_period_breaks, theme_seaborn_,
				  			   output_dir):
	Context = HighlightsTimeseriesContext
	View = HighlightsTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/highlights.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def generate_notes_report(session, start_date, end_date, courses,
			  			   period_breaks, minor_period_breaks, theme_seaborn_,
			  			   output_dir):
	Context = NoteEventsTimeseriesContext
	View = NoteEventsTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/notes.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def generate_resource_views_report(session, start_date, end_date, courses,
			  			   period_breaks, minor_period_breaks, theme_seaborn_,
			  			   output_dir):
	Context = ResourceViewsTimeseriesContext
	View = ResourceViewsTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/resource_views.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def generate_topics_report(session, start_date, end_date, courses,
			  			   period_breaks, minor_period_breaks, theme_seaborn_,
			  			   output_dir):
	Context = TopicsTimeseriesContext
	View = TopicsTimeseriesReportView
	rml, data = build_rml(Context, View, session, start_date, end_date, courses,
			  		period_breaks, minor_period_breaks, theme_seaborn_)

	filepath = '%s/topics.pdf' % output_dir
	report = create_pdf_file_from_rml(rml, filepath)
	cleanup_temporary_file(data)
	return report

def main():
	# Parse command line args
	args = _parse_args()

	_setup_configs()


	context = config.ConfigurationMachine()
	xmlconfig.registerCommonDirectives(context)
	xmlconfig.file('configure.zcml', package=nti.analytics_pandas, context=context)

	# Create the output directory if it does not exist
	if not os.path.exists(args.output):
		os.mkdir(args.output)

	db = DBConnection()

	"""
	only for test 
	"""
	start_date = '2015-10-05'
	end_date = '2015-10-20'
	courses = ['1068', '1096', '1097', '1098', '1099']
	period_breaks = '1 day'
	minor_period_breaks = None
	theme_seaborn_ = True

	generate_bookmarks_report(db.session, start_date, end_date, courses,
		  					  period_breaks, minor_period_breaks, theme_seaborn_,
		  					  args.output)

	generate_assessments_report(db.session, start_date, end_date, courses,
			  					period_breaks, minor_period_breaks, theme_seaborn_,
			  					args.output)

	generate_enrollments_report(db.session, start_date, end_date, courses,
			  					period_breaks, minor_period_breaks, theme_seaborn_,
			  					args.output)

	generate_forums_report(db.session, start_date, end_date, courses,
		  				   period_breaks, minor_period_breaks, theme_seaborn_,
		  				   args.output)

	generate_highlights_report(db.session, start_date, end_date, courses,
			  				   period_breaks, minor_period_breaks, theme_seaborn_,
			  				   args.output)

	generate_notes_report(db.session, start_date, end_date, courses,
		  				  period_breaks, minor_period_breaks, theme_seaborn_,
		  				  args.output)

	generate_resource_views_report(db.session, start_date, end_date, courses,
				  				   period_breaks, minor_period_breaks, theme_seaborn_,
				  				   args.output)

	generate_topics_report(db.session, start_date, end_date, courses,
		  				  period_breaks, minor_period_breaks, theme_seaborn_,
		  				  args.output)

	db.close_session()


if __name__ == '__main__':  # pragma: no cover
	main()