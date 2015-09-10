#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: common.py 72633 2015-09-09 15:00:23Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd
import numpy as np 

from .resources import QueryResources

def add_resource_type_(session,dataframe):
	if 'resource_id' in dataframe.columns:
		resources_id = np.unique(dataframe['resource_id'].values.ravel()).tolist()
		qr = QueryResources(session)
		resources_df = qr.get_resources_ds_id_given_id(resources_id)
		resources_df = qr.add_resource_type(resources_df)
		resources_df = resources_df[['resource_id', 'resource_type']]
		new_df = dataframe.merge(resources_df)
		return new_df
	return dataframe

