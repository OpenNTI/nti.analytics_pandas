#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import create_engine

from pandas import DataFrame

from ..utils.string_folder import StringFolder

def create_engine_mysql(db_user='root', pwd=None, host='localhost', port='3306',
						db_name='Analytics'):
	"""
	create engine to access mysql db
	"""
	if pwd is None:
		engine_string = u'mysql+pymysql://%s@%s:%s/%s' % (db_user, host, port, db_name)
	else:
		engine_string = u'mysql+pymysql://%s:%s@%s:%s/%s' % (db_user, pwd, host, port, db_name)
	return create_engine(engine_string)

def build_data_frame(engine, query):
	with engine.connect() as connection:
		# Execute the query against the database
		results = (connection.execution_options(stream_results=True).execute(query))
		# dataframe = DataFrame(iter(results))
		dataframe = DataFrame(string_folding_wrapper(results))
		dataframe.columns = results.keys()
	connection.close()
	return dataframe

def string_folding_wrapper(query_results):
	"""
	source : http://www.mobify.com/blog/sqlalchemy-memory-magic/
	This generator yields rows from the results as tuples,
	with all string values folded.
	"""
	# Get the list of keys so that we build tuples with all
	# the values in key order.
	keys = query_results.keys()
	folder = StringFolder()
	for row in query_results:
		yield tuple(
			folder.fold_string(row[key])for key in keys
		)
