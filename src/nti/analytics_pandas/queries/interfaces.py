#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface

class IQueryTopicsCreated(interface.Interface):
	"""
	a utility to query all topics created given a period of time and return the result
	in a DataFrame
	"""

class IQueryTopicsLikes(interface.Interface):
	"""
	query all topics likes given a period of time and return the result in a DataFrame
	"""

class IQueryTopicsFavorites(interface.Interface):
	"""
	query all topics likes given a period of time and store the result in a DataFrame
	"""

class IQueryTopicsViewed(interface.Interface):
	"""
	query all topics likes given a period of time and return the result in a DataFrame
	"""

class IQueryForumsCreated(interface.Interface):
	"""
	query all forums created given a period of time, store query result in a DataFrame
	"""

class IQueryForumCommentsCreated(interface.Interface):
	"""
	query all forum's comments created given a period of time, store query result in a
	DataFrame
	"""

class IQueryForumCommentsLikes(interface.Interface):
	"""
	query all forum's comments likes given a period of time, store query result
	in a DataFrame
	"""

class IQueryForumCommentsFavorites(interface.Interface):
	"""
	query all forum's comments  favorites given a period of time, store query result
	in a DataFrame
	"""
