#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from pandas import DataFrame

def add_timestamp_period_date(df, index_name=None):
	if index_name is not None : df.set_index(index_name, inplace=True)
	df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime('%Y-%m-%d'))
	df.reset_index(inplace=True)
	return df