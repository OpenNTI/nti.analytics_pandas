#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest
import os
import importlib
import glob
import pandas

# there is a bug in matplotlib 1.5.0 that is requiring a back end in OSX
# https://github.com/pypa/virtualenv/issues/54
# https://github.com/pypa/virtualenv/issues/609
# (reported in http://matplotlib.org/faq/virtualenv_faq.html#osx)
# as work around include the last two lines below execute
# echo "backend: TXAgg" > ~/.matplotlib/matplotlibrc
# import matplotlib
# matplotlib.use('PS')

from zope.testing import cleanup as testing_cleanup

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

from nti.analytics_database import *

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

from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine as sqlalchemy_create_engine

def create_engine(dburi='sqlite://', pool_size=30, max_overflow=10, pool_recycle=300):
    try:
        if dburi == 'sqlite://':
            result = sqlalchemy_create_engine(dburi,
                                              connect_args={'check_same_thread': False},
                                              poolclass=StaticPool)

        else:
            result = sqlalchemy_create_engine(dburi,
                                              pool_size=pool_size,
                                              max_overflow=max_overflow,
                                              pool_recycle=pool_recycle)
    except TypeError:
        # SQLite does not use pooling anymore.
        result = sqlalchemy_create_engine(dburi)
    return result


def create_sessionmaker(engine, autoflush=False, twophase=False):
    result = sessionmaker(bind=engine,
                          autoflush=autoflush,
                          twophase=twophase)
    return result


def create_session(sessionmaker):
    return scoped_session(sessionmaker)

from nti.analytics_database import Base

# Only a few of the tables appear in the metadata, 
# so we have to import some modules so they are known
from nti.analytics_database.mime_types import FileMimeTypes

class AnalyticsPandasTestBase(unittest.TestCase):

    def setUp(self):
        dburi="sqlite://"
        self.engine = create_engine(dburi=dburi)
        self.metadata = getattr(Base, 'metadata')
        self.metadata.create_all(bind=self.engine)
        self._read_sample_data(self.engine)
        self.sessionmaker = create_sessionmaker(self.engine)
        self.session = create_session(self.sessionmaker)

    def tearDown(self):
        self.session.commit()
        self.session.close()

    def _read_sample_data(self, engine):
        # run from nti.analytics_pandas directory
        import re
        path = os.path.join(os.getcwd(), "src/nti/analytics_pandas/tests/testdb")
        for file in glob.glob(os.path.join(path,"*.csv")):
            try:
                tablename = re.split("\W+", file)[-2]
                df = pandas.read_csv(file)
                df.to_sql(con=engine, name=tablename, if_exists='replace')
            except:
                continue