#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: pdf_generator.py 73213 2015-09-17 18:48:03Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from z3c.rml import rml2pdf
