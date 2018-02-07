#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.analytics_database.resources import Resources

from nti.analytics_pandas import MessageFactory as _

from nti.analytics_pandas.queries.mixins import TableQueryMixin

from nti.analytics_pandas.utils.dataframe_operation import orm_dataframe

logger = __import__('logging').getLogger(__name__)


class QueryResources(TableQueryMixin):

    table = Resources

    def get_all_resources(self):
        r = self.table
        query = self.session.query(r.resource_id,
                                   r.resource_ds_id,
                                   r.resource_display_name,
                                   r.max_time_length)
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def get_resources_ds_id_given_id(self, resource_id=()):
        r = self.table
        query = self.session.query(r.resource_id,
                                   r.resource_ds_id).filter(r.resource_id.in_(resource_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def get_resources_given_id(self, resources_id=None):
        r = self.table
        query = self.session.query(r.resource_id,
                                   r.resource_ds_id,
                                   r.resource_display_name,
                                   r.max_time_length).filter(r.resource_id.in_(resources_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    def get_resource_display_name_given_id(self, resources_id=None):
        r = self.table
        query = self.session.query(r.resource_id,
                                   r.resource_display_name).filter(r.resource_id.in_(resources_id))
        dataframe = orm_dataframe(query, self.columns)
        return dataframe

    @classmethod
    def _label_resource_type(cls, resource_ds_id):
        # video
        if '.ntivideo.' in resource_ds_id:
            return _(u'video')
        elif 'NTISlideVideo' in resource_ds_id:
            return _(u'slide video')

        # relatedwork
        if '.relatedworkref.' in resource_ds_id:
            if 'requiredreadings' in resource_ds_id:
                return _(u'required readings')
            elif 'textbook' in resource_ds_id:
                return _(u'textbook')
            elif 'reading_' in resource_ds_id:
                return _(u'reading')
            elif 'lecture' in resource_ds_id:
                return _(u'related work lecture')
            elif 'hw' in resource_ds_id:
                return _(u'homework')
            elif 'syllabus' in resource_ds_id:
                return _(u'syllabus')
            elif 'problem' in resource_ds_id:
                return _(u'problems')
            else:
                return _(u'relatedworkref')

        # assignment
        if 'naq.asg.assignment:' in resource_ds_id:
            return _(u'assignment')

        # question set
        if 'naq.set.qset' in resource_ds_id:
            return _(u'question set')

        # quiz
        if '.naq.qid.' in resource_ds_id:
            if u'self_check' in resource_ds_id:
                return _(u'self check question')
            elif u'quiz' in resource_ds_id:
                return _(u'quiz question')
            else:
                return _(u'question')
        elif 'quiz' in resource_ds_id:
            return _(u'quiz')

        # self assessment
        if 'self_assessment' in resource_ds_id:
            return _(u'self assessment')

        # self check
        if 'self_check' in resource_ds_id or 'check_yourself' in resource_ds_id:
            return _(u'self check')

        # pre lab workbook
        if 'pre_lab_workbook:' in resource_ds_id:
            return _(u'pre lab workbook')

        # honor code
        if 'honor_code' in resource_ds_id:
            return _(u'honor code')

        # lecture
        if 'lec:' in resource_ds_id:
            return _(u'lecture')

        # reading
        if 'reading:' in resource_ds_id:
            return _(u'reading')

        # discussion
        if 'discussion:' in resource_ds_id or u'discussions:' in resource_ds_id:
            return _(u'discussion')
        elif 'In_Class_Discussions' in resource_ds_id:
            return _(u'in class discussion')
        elif 'section:' in resource_ds_id or u'sec:' in resource_ds_id:
            return _(u'section')

        # nti card
        if 'nticard' in resource_ds_id:
            return _(u'nticard')

        # timeline
        if 'JSON:Timeline' in resource_ds_id:
            return _(u'timeline')

        if 'practice_problems' in resource_ds_id:
            return _(u'practice problems')

        if 'problem' in resource_ds_id:
            return _(u'problems')

        return _(u'unknown')

    def add_resource_type(self, dataframe):
        index = dataframe['resource_ds_id']
        # pylint: disable=unnecessary-lambda
        dataframe['resource_type'] = index.apply(lambda x: self._label_resource_type(x))
        return dataframe
