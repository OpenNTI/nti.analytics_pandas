#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: report.py 58552 2015-01-29 23:10:30Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import codecs
import logging
import argparse

from ..databases import DBConnection

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

def _parse_args():
	arg_parser = argparse.ArgumentParser( description="NTI Analytics" )
	arg_parser.add_argument( '-o', '--output', 
							 default='output',
							 help="The output directory. The default is: %s" % 'output' )
	return arg_parser.parse_args()

def _configure_logging(level='INFO'):
	numeric_level = getattr(logging, level.upper(), None)
	numeric_level = logging.INFO if not isinstance(numeric_level, int) else numeric_level
	logging.basicConfig(level=numeric_level)

def _setup_configs():
	_configure_logging()
	
def main():
	# Parse command line args
	args = _parse_args()

	_setup_configs()
	
	# Create the output directory if it does not exist
	if not os.path.exists( args.output ):
		os.mkdir( args.output )

	db = DBConnection()
	print(db.session)


if __name__ == '__main__': # pragma: no cover
	main()
