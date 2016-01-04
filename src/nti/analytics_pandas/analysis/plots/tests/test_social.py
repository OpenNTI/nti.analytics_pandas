#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.social import ContactsAddedTimeseries
from nti.analytics_pandas.analysis.social import ContactsEventsTimeseries
from nti.analytics_pandas.analysis.social import ContactsRemovedTimeseries

from nti.analytics_pandas.analysis.plots.social import ContactsEventsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestContactsEventsTimeseriesPlot(AnalyticsPandasTestBase):
	def test_combine_events(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date, period=period)
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date, period=period)
		cet = ContactsEventsTimeseries(cat=cat, crt=crt)
		cetp = ContactsEventsTimeseriesPlot(cet)
		_ = cetp.combine_events(period_breaks='1 week')
		assert_that(len(_), equal_to(3))