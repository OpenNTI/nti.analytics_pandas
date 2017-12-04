#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id:
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface


class IDBConnection(interface.Interface):
    """
    Representation of a pandas analyitcs database
    """

    engine = interface.Attribute("SQLAlchemy engine")
    session = interface.Attribute("SQLAlchemy session")
    sessionmaker = interface.Attribute("SQLAlchemy session maker")

    def close():
        """
        close the session
        """