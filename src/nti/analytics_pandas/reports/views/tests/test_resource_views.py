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

from nti.analytics_pandas.reports.views.resource_views import View
from nti.analytics_pandas.reports.views.resource_views import Context

from nti.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.common.property import Lazy

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViews(AnalyticsPandasTestBase):

	render_name = '../templates/resource_views.rml'

	def setUp(self):
		super(TestResourceViews, self).setUp()

	@Lazy
	def template_path(self):
		path = os.path.join(os.path.dirname(__file__), '../' + self.render_name)
		return path

	@property
	def template(self):
		result = ViewPageTemplateFile(self.template_path,
									  auto_reload=(False,),
									  debug=False)
		return result
	
	def test_generic(self):
		assert_that(os.path.exists(self.template_path), is_(True))
		context = Context()
		view = View(context)
		data = view._build_data('Bleach')
		system = {'view':view, 'context':context}
		system.update(data)
		result = self.template.bind(view)(**system)
		assert_that(result, contains_string('Bleach'))
