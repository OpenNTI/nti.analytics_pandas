#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component

from .db_connection import DBConnection
from .interfaces import IDBConnection

def get_analytics_db(strict=True):
    if strict:
        return component.getUtility(IDBConnection)
    else:
        return component.queryUtility(IDBConnection)