#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pandas import DataFrame

from zope import interface

from nti.analytics_pandas.databases.interfaces import IDBConnection

from nti.analytics_pandas.utils.string_folder import StringFolder

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IDBConnection)
class DBConnection(object):

    def __init__(self, db):
        self.db = db

    @property
    def engine(self):
        return self.db.engine

    @property
    def sessionmaker(self):
        return self.db.sessionmaker

    @property
    def session(self):
        return self.db.session

    def close(self):
        self.session.close()


def build_data_frame(engine, query):
    with engine.connect() as connection:
        # Execute the query against the database
        prepared = connection.execution_options(stream_results=True)
        results = prepared.execute(query)
        # dataframe = DataFrame(iter(results))
        dataframe = DataFrame(string_folding_wrapper(results))
        dataframe.columns = results.keys()
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
        yield tuple(folder.fold_string(row[key])for key in keys)
