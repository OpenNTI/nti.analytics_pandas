#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.chats import ChatsInitiatedTimeseries
from nti.analytics_pandas.analysis.chats import ChatsJoinedTimeseries
from nti.analytics_pandas.analysis.plots.chats import ChatsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestChatsPlot(AnalyticsPandasTestBase):

	def test_explore_chats_initiated(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		cit = ChatsInitiatedTimeseries(self.session, start_date, end_date)
		citp = ChatsTimeseriesPlot(cit=cit)
		_ = citp.explore_chats_initiated()
		assert_that(len(_), equal_to(3))


	def test_analyze_application_types(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		cit = ChatsInitiatedTimeseries(self.session, start_date, end_date)
		citp = ChatsTimeseriesPlot(cit=cit)
		_ = citp.analyze_application_types()
		assert_that(len(_), equal_to(3))