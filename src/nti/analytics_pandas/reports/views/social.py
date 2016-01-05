#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: social.py 78996 2015-12-15 14:34:05Z egawati.panjei $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import ContactsEventsTimeseriesPlot
from ...analysis import ContactsAddedTimeseriesPlot
from ...analysis import ContactsRemovedTimeseriesPlot
from ...analysis import FriendsListsMemberAddedTimeseriesPlot

from ...analysis import ContactsEventsTimeseries
from ...analysis import ContactsAddedTimeseries
from ...analysis import ContactsRemovedTimeseries
from ...analysis import FriendsListsMemberAddedTimeseries

from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class SocialTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None,
				 period_breaks=None, minor_period_breaks=None, theme_seaborn_=True,
				 number_of_most_active_user=10, period='daily'):
		self.session = session
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_seaborn_ = theme_seaborn_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user
		self.period = period

Context = SocialTimeseriesContext

class SocialTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Social Related Events Report')

	def _build_data(self, data=_('sample social related events report')):
		keys = self.options.keys()
		if 'has_contacts_added_data' not in keys:
			self.options['has_contacts_added_data'] = False
		self.options['data'] = data
		return self.options

	def __call__(self):
		data = {}
		self.cat = ContactsAddedTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   period=self.context.period)
		
		if self.cat.dataframe.empty:
			self.options['has_contacts_added_data'] = False
		else:
			self.options['has_contacts_added_data'] = True
			data = self.generate_contacts_added_plots(data)
		self._build_data(data)
		return self.options

	def generate_contacts_added_plots(self, data):
		self.catp = ContactsAddedTimeseriesPlot(self.cat)
		data = self.get_contacts_added_plots(data)
		return data

	def get_contacts_added_plots(self, data):
		plots = self.catp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_seaborn_)
		if plots:
			data['contacts_added'] = build_plot_images_dictionary(plots)
		return data

View = SocialTimeseriesReport = SocialTimeseriesReportView