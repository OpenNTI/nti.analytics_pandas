#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from pandas import DataFrame

from pandas.core.categorical import Categorical


def get_values_of_series_categorical_index_(categorical_series):
    index = categorical_series.index.values
    if isinstance(index, Categorical) or hasattr(index, 'get_values'):
        return index.get_values()
    return index


def cast_columns_as_category_(df, list_of_columns):
    if len(df.index) > 0:
        for column in list_of_columns or ():
            df[column] = df[column].astype('category')
    return df


def create_row(obj, columns):
    dictionary = {
        col: getattr(obj, col) for col in columns if hasattr(obj, col)
    }
    return dictionary


def orm_dataframe(orm_query, columns):
    """
    Takes sqlachemy orm query and a list of its columns and transform it 
    to pandas dataframe
    """
    result = DataFrame(create_row(i, columns) for i in orm_query)
    return result
