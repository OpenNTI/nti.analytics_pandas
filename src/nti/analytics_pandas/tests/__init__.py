#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

# echo "backend: TXAgg" > ~/.matplotlib/matplotlibrc
# import matplotlib
# matplotlib.use('PS')

import os
import re
import glob

import pandas

from zope import component

from zope.testing import cleanup as testing_cleanup

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

from nti.analytics_database.interfaces import IAnalyticsDatabase


def read_sample_data(engine):
    # run from nti.analytics_pandas directory
    path = os.path.join(os.path.dirname(__file__), "testdb")
    for source in glob.glob(os.path.join(path, "*.csv")):
        try:
            tablename = re.split(r"\W+", source)[-2]
            df = pandas.read_csv(source)
            df.to_sql(con=engine, name=tablename, if_exists='replace')
        except Exception:  # pylint: broad-except
            pass


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 GCLayerMixin,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.analytics_pandas',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()
        cls.database = component.getUtility(IAnalyticsDatabase)
        read_sample_data(cls.database.engine)

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        testing_cleanup.cleanUp()
        cls.database.session.close()

    @classmethod
    def testSetUp(cls, test=None):
        pass

    @classmethod
    def testTearDown(cls):
        pass


import unittest


class AnalyticsPandasTestBase(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    @property
    def session(self):
        # pylint: disable=no-member
        return self.layer.database.session

    @property
    def engine(self):
        # pylint: disable=no-member
        return self.layer.database.engine

    @property
    def sessionmaker(self):
        return self.layer.database.sessionmaker
