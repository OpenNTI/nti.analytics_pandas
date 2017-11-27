#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.analytics_pandas import MessageFactory

from nti.analytics_pandas.analysis.plots.assessments import AssignmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import AssignmentsTakenTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import AssessmentEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import SelfAssessmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import SelfAssessmentsTakenTimeseriesPlot

from nti.analytics_pandas.analysis.plots.bookmarks import BookmarksTimeseriesPlot

from nti.analytics_pandas.analysis.plots.chats import ChatsTimeseriesPlot

from nti.analytics_pandas.analysis.plots.enrollments import CourseDropsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseEnrollmentsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseCatalogViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseEnrollmentsEventsTimeseriesPlot

from nti.analytics_pandas.analysis.plots.forums import ForumsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCreatedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumCommentLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCommentsCreatedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumCommentFavoritesTimeseriesPlot

from nti.analytics_pandas.analysis.plots.highlights import HighlightsCreationTimeseriesPlot

from nti.analytics_pandas.analysis.plots.notes import NotesViewTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NoteLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NoteFavoritesTimeseriesPlot

from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileViewEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileActivityViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileMembershipViewsTimeseriesPlot

from nti.analytics_pandas.analysis.plots.resource_views import ResourceViewsTimeseriesPlot

from nti.analytics_pandas.analysis.plots.social import ContactsAddedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.social import ContactsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.social import ContactsRemovedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.social import FriendsListsMemberAddedTimeseriesPlot

from nti.analytics_pandas.analysis.plots.topics import TopicLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicsCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicFavoritesTimeseriesPlot

from nti.analytics_pandas.analysis.plots.videos import VideoEventsTimeseriesPlot
