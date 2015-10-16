#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import contains_string

import os

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
	
	def xtest_generic_rml(self):
		path = self.resource_views_rml
		assert_that(os.path.exists(path), is_(True))
		view = View(Context())
		view._build_data('Bleach')
		rml = self.template(path).bind(view)()
		assert_that(rml, contains_string('Bleach'))
	
	def test_generic_pdf(self):
		path = self.std_report_layout_rml
		assert_that(os.path.exists(path), is_(True))
		context = Context()
		view = View(context)
		data = view._build_data('Bleach')
		system = {'view':view, 'context':context}
		system.update(data)
		#from IPython.core.debugger import Tracer; Tracer()()
		rml = self.template(path).bind(view)(**system)
		assert_that(rml, contains_string('Bleach'))
		
		#from IPython.core.debugger import Tracer; Tracer()()
		pdf_stream = rml2pdf.parseString( rml )
		result = pdf_stream.read()
		print(result)