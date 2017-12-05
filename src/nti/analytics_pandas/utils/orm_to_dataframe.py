#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pandas import DataFrame

logger = __import__('logging').getLogger(__name__)


def create_row(obj, columns):
    dictionary = {
        col: getattr(obj, col) for col in columns if hasattr(obj, col)
    }
    return dictionary


def orm_dataframe(orm_query, columns):
    """
    Takes sqlachemy orm query and a list of its columns and transform it to pandas dataframe
    """
    result = DataFrame([create_row(i, columns) for i in orm_query])
    return result
