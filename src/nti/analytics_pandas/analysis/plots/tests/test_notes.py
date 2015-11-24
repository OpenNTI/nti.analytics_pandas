#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.notes import NoteLikesTimeseries
from nti.analytics_pandas.analysis.notes import NotesViewTimeseries
from nti.analytics_pandas.analysis.notes import NotesEventsTimeseries
from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries
from nti.analytics_pandas.analysis.notes import NoteFavoritesTimeseries

from nti.analytics_pandas.analysis.plots.notes import NoteLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesViewTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NoteFavoritesTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestNotesCreationPlot(AnalyticsPandasTestBase):

	def test_explore_events_notes_creation(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.explore_events()

	def test_analyze_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_device_types()

	def test_analyze_resource_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_resource_types()

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.plot_the_most_active_users()

	def test_analyze_sharing_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_sharing_types()

	def test_analyze_notes_created_on_videos(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_notes_created_on_videos(period_breaks='1 day', minor_period_breaks='None')

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_events_per_course_sections()

class TestNoteViewsPlot(AnalyticsPandasTestBase):

	def test_analyze_total_events_based_on_sharing_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_sharing_type(period_breaks='1 week')

	def test_analyze_total_events_based_on_device_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_device_type(period_breaks='1 week')

	def test_analyze_total_events_based_on_enrollment_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_enrollment_type(period_breaks='1 week')

	def test_analyze_total_events_based_on_resource_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_resource_type(period_breaks='1 week')

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.plot_the_most_active_users()

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.explore_events(period_breaks='1 week')

	def test_analyze_unique_events_based_on_sharing_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_unique_events_based_on_sharing_type(period_breaks='1 week')

	def test_analyze_total_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_per_course_sections()

	def test_plot_the_most_viewed_notes_and_its_author(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.plot_the_most_viewed_notes_and_its_author()

class TestNoteLikesPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		_ = nltp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		_ = nltp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_enrollment_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		_ = nltp.analyze_events_per_enrollment_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_resource_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		_ = nltp.analyze_events_per_resource_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		_ = nltp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

class TestNoteFavoritesPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		_ = nftp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		_ = nftp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_enrollment_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		_ = nftp.analyze_events_per_enrollment_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_resource_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		_ = nftp.analyze_events_per_resource_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		_ = nftp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

class TestNotesEventsPlot(AnalyticsPandasTestBase):

	def test_notes_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)

		net = NotesEventsTimeseries(nct, nvt, nlt, nft)
		netp = NotesEventsTimeseriesPlot(net)
		_ = netp.explore_all_events()
