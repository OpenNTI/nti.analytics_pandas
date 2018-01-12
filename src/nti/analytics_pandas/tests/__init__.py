#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

# echo "backend: TXAgg" > ~/.matplotlib/matplotlibrc
# import matplotlib
# matplotlib.use('PS')

from zope.testing import cleanup as testing_cleanup

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 GCLayerMixin,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.analytics_pandas',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        testing_cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, test=None):
        pass

    @classmethod
    def testTearDown(cls):
        pass


import os
import re
import glob
import unittest

import pandas

from zope import component

from nti.analytics_database.database import AnalyticsDB

from nti.analytics_database.interfaces import IAnalyticsDB

# Only a few of the tables appear in the metadata,
# so we have to import some modules so they are known
from nti.analytics_database.mime_types import FileMimeTypes


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


class AnalyticsPandasTestBase(unittest.TestCase):

    def setUp(self):
        self.db = AnalyticsDB(dburi="sqlite://", 
                              defaultSQLite=True,
                              autocommit=True)
        component.getGlobalSiteManager().registerUtility(self.db, IAnalyticsDB)
        self._read_sample_data(self.db.engine)

    def tearDown(self):
        component.getGlobalSiteManager().unregisterUtility(self.db, IAnalyticsDB)
        # pylint: disable=no-member
        self.db.session.commit()
        self.db.session.close()

    def _read_sample_data(self, engine):
        # run from nti.analytics_pandas directory
        read_sample_data(engine)
    
    @property
    def session(self):
        # pylint: disable=no-member
        return self.db.session
    
    @property
    def engine(self):
        # pylint: disable=no-member
        return self.db.engine
    
    @property
    def sessionmaker(self):
        return self.db.sessionmaker
