#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: orm_to_dataframe.py 70252 2015-08-10 15:22:32Z egawati.panjei $
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from pandas import DataFrame

def orm_dataframe(orm_query, columns):
	"""
	takes sqlachemy orm query and a list of its columns and transform it to pandas dataframe
	"""
	def create_row(i):
		dictionary = {}
		for col in columns:
			if hasattr(i, col) : dictionary[col] = getattr(i, col)
		return dictionary
	return DataFrame([create_row(i) for i in orm_query])