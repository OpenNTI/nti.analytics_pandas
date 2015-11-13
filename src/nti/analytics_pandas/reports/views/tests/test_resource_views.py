#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than
from hamcrest import contains_string

import os
import shutil

from z3c.rml import rml2pdf

from nti.analytics_pandas.reports.views.resource_views import View
from nti.analytics_pandas.reports.views.resource_views import Context

from nti.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.common.property import Lazy

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViews(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestResourceViews, self).setUp()
	
	@Lazy
	def std_report_layout_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/std_report_layout.rml')
		return path

	@Lazy
	def resource_views_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/resource_views.rml')
		return path

	def template(self, path):
		result = ViewPageTemplateFile(path,
									  auto_reload=(False,),
									  debug=False)
		return result
	
	def test_resource_views_rml(self):
		# make sure  template exists
		path = self.resource_views_rml
		assert_that(os.path.exists(path), is_(True))
		
		# prepare view and context
		context = Context()
		view = View(context)
		view._build_data('Bleach')
		
		rml = self.template(path).bind(view)()
		assert_that(rml, contains_string('Bleach'))

	def test_std_report_layout_rml(self):
		# make sure  emplate exists
		path = self.std_report_layout_rml
		assert_that(os.path.exists(path), is_(True))
		
		# prepare view and context
		context = Context()
		view = View(context)
		view._build_data('Bleach')
		system = {'view':view, 'context':context}
		rml = self.template(path).bind(view)(**system)
		assert_that(rml, contains_string('Bleach'))
		
		pdf_stream = rml2pdf.parseString(rml)
		result = pdf_stream.read()
		assert_that(result, has_length(greater_than(1)))

	def test_generate_pdf_from_rml(self):
		# make sure  emplate exists
		path = self.std_report_layout_rml
		assert_that(os.path.exists(path), is_(True))
		
		# prepare view and context
		context = Context()
		view = View(context)
		view._build_data('Bleach')
		system = {'view':view, 'context':context}
		rml = self.template(path).bind(view)(**system)
		assert_that(rml, contains_string('Bleach'))
		
		pdf_stream = rml2pdf.parseString(rml)
		pdf_stream.seek(0)
		fd = open('test_resource_views.pdf', 'w')
		shutil.copyfileobj(pdf_stream, fd)
		
		assert_that(os.path.exists('test_resource_views.pdf'), is_(True))


