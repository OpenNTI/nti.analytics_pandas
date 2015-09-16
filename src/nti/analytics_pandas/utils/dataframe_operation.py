#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas

def get_values_of_series_categorical_index_(categorical_series):
	index = categorical_series.index.values
	if isinstance(index, pandas.core.categorical.Categorical):
		return index.get_values()


