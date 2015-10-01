#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pytz
import textwrap
from datetime import datetime

from zope import interface

from z3c.pagelet.browser import BrowserPagelet

from .interfaces import IPDFReportView

def _adjust_date( date ):
	"""
	Takes a date and returns a timezoned datetime
	"""
	utc_date = pytz.utc.localize( date )
	cst_tz = pytz.timezone('US/Central')
	return utc_date.astimezone( cst_tz )

def adjust_timestamp( timestamp ):
	"""
	Takes a timestamp and returns a timezoned datetime
	"""
	date = datetime.utcfromtimestamp( timestamp )
	return _adjust_date( date )

def _format_datetime( local_date ):
	"""Returns a string formatted datetime object"""
	return local_date.strftime("%Y-%m-%d %H:%M")

@interface.implementer(IPDFReportView)
class AbstractReportView(BrowserPagelet):

	def __init__(self, context, request):
		self.options = {}
		BrowserPagelet.__init__(self, context, request)

	def generate_footer(self):
		date = _adjust_date(datetime.utcnow())
		date = date.strftime('%b %d, %Y %I:%M %p')
		title = self.report_title
		course = self.course_name()
		student = getattr(self, 'student_user', '')
		return "%s %s %s %s" % (title, course, student, date)

	def wrap_text(self, text, size):
		return textwrap.fill(text, size)
