#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from nti.analytics_database.interfaces import IAnalyticsDatabase

from nti.analytics_pandas.databases.db_connection import DBConnection

from nti.analytics_pandas.databases.interfaces import IDBConnection

logger = __import__('logging').getLogger(__name__)


def get_analytics_db(strict=True):
    if strict:
        database = component.getUtility(IAnalyticsDatabase)
    else:
        database = component.queryUtility(IDBConnection)
    if database is not None:
        return DBConnection(database)
    return None
