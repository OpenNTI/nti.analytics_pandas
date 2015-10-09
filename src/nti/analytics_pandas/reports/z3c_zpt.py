#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from z3c.pt.pagetemplate import ViewPageTemplateFile

class _ViewPageTemplateFileWithLoad(ViewPageTemplateFile):
	"""
	Enables the load: expression type for convenience.
	"""
	# NOTE: We cannot do the rational thing and copy this
	# and modify our local value. This is because
	# certain packages, notably z3c.macro,
	# modify the superclass's value; depending on the order
	# of import, we may or may not get that change.
	# So we do the bad thing too and modify the superclass also

	@property
	def builtins(self):
		d = super(_ViewPageTemplateFileWithLoad,self).builtins
		d['__loader'] = self._loader
		# https://github.com/malthe/chameleon/issues/154
		# That's been fixed, so we should no longer
		# need to do this:
		## We try to get iteration order fixed here:
		#result = OrderedDict()
		#for k in sorted(d.keys()):
		#	result[k] = d[k]
		#return result
		return d

# Re-export our version
ViewPageTemplateFile = _ViewPageTemplateFileWithLoad
