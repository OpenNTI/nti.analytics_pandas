#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import os
import re
import glob
import unittest

import pandas

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


from sqlalchemy import create_engine as sqlalchemy_create_engine

from sqlalchemy.pool import StaticPool

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


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


def create_session(session_maker):
    return scoped_session(session_maker)


from nti.analytics_database import Base

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
        dburi = "sqlite://"
        self.engine = create_engine(dburi=dburi)
        self.metadata = getattr(Base, 'metadata')
        self.metadata.create_all(bind=self.engine)
        self._read_sample_data(self.engine)
        self.sessionmaker = create_sessionmaker(self.engine)
        self.session = create_session(self.sessionmaker)

    def tearDown(self):
        # pylint: disable=no-member
        self.session.commit()
        self.session.close()

    def _read_sample_data(self, engine):
        # run from nti.analytics_pandas directory
        read_sample_data(engine)
