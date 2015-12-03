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

from .views import create_pdf_file_from_rml
from .views import cleanup_temporary_file

from .z3c_zpt import ViewPageTemplateFile

from ..databases import DBConnection

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser(description="NTI Analytics")
	arg_parser.add_argument('start_date',
							 help="Report duration start date, use the format %s" %'yyyy-mm-dd')
	arg_parser.add_argument('end_date',
							 help="Report duration end date, use the format %s" %'yyyy-mm-dd')
	arg_parser.add_argument('courses',
							 help="Course/s ID. For example %s" %'1068, 1096, 1097, 1098, 1099')
	arg_parser.add_argument('-pb', '--period_breaks',
							 default='1 week',
							 help="Set period breaks on generated plots. The default is %s" %"'1 week'")
	arg_parser.add_argument('-mpb', '--minor_period_breaks',
							 default= None,
							 help="Set minor period breaks on generated plots. The default is %s" %"'1 day'")
	arg_parser.add_argument('-ts', '--theme_seaborn',
							 default=True,
							 help="Seaborn theme for generated plots. The default it is 1 (true)")
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

def _configure_config():
	context = config.ConfigurationMachine()
	xmlconfig.registerCommonDirectives(context)
	xmlconfig.file('configure.zcml', package=nti.analytics_pandas, context=context)

def str2bool(v):
	return v.lower() in ("yes", "true", "t", "1")

def process_args():
	args = _parse_args()
	args_dict = {}
	args_dict['start_date'] = args.start_date 
  	args_dict['end_date'] = args.end_date 
  	
  	if ',' in args.courses:
  		args_dict['courses'] = args.courses.split(',')
  	else:
  		args_dict['courses'] = args.courses.split()
	
	args_dict['period_breaks'] = args.period_breaks
	args_dict['minor_period_breaks'] = args.minor_period_breaks
	
	if isinstance(args.theme_seaborn, bool):
		args_dict['theme_seaborn'] = args.theme_seaborn
	else:
		args_dict['theme_seaborn'] = str2bool(args.theme_seaborn)
	
	args_dict['output'] = args.output
	return args_dict


class Report(object):
	def __init__(self, Context, View, start_date, end_date, courses,
				 period_breaks, minor_period_breaks,theme_seaborn_, filepath):
		self.db = DBConnection()
		self.context = Context(self.db.session, start_date, end_date, courses,
					  		   period_breaks, minor_period_breaks, theme_seaborn_)
		self.view = View(self.context)
		self.filepath = filepath

	def std_report_layout_rml(self):
		path = os.path.join(os.path.dirname(__file__), 'templates/std_report_layout.rml')
		return path

	def template(self, path):
		result = ViewPageTemplateFile(path,
									  auto_reload=(False,),
									  debug=False)
		return result	
	
	def build(self):
		self.view()
		path = self.std_report_layout_rml()
		system = {'view':self.view, 'context':self.context}
		rml = self.template(path).bind(self.view)(**system)
		data = self.view.options['data']
		report = create_pdf_file_from_rml(rml, self.filepath)
		cleanup_temporary_file(data)
		self.db.session.close()
		return report
