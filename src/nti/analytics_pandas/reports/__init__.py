#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
from six import string_types

from zope.browserpage import viewpagetemplatefile

from zope.pagetemplate.pagetemplatefile import package_home

# Make viewlets use our version of page template files
# Unfortunately, the zope.browserpage VPT is slightly
# incompatible in calling convention
from zope.viewlet import viewlet

from z3c.template import template

from .z3c_zpt import ViewPageTemplateFile

# Best to use a class not a function to avoid changing
# calling depth
class _VPT(ViewPageTemplateFile):

    def __init__(self, filename, _prefix=None, content_type=None):
        path = _prefix
        if not isinstance(path, string_types) and path is not None:
            # zope likes to pass the globals
            path = package_home(path)

        debug = os.getenv('DEBUG_TEMPLATES')
        auto_reload = os.getenv('RELOAD_TEMPLATES')
        ViewPageTemplateFile.__init__(self, filename, path=path, content_type=content_type,
                                      auto_reload=auto_reload,
                                      debug=debug)

if viewlet.ViewPageTemplateFile is viewpagetemplatefile.ViewPageTemplateFile:
    logger.debug("Monkey-patching zope.viewlet to use z3c.pt")
    viewlet.ViewPageTemplateFile = _VPT
    
if template.ViewPageTemplateFile is viewpagetemplatefile.ViewPageTemplateFile:
    logger.debug("Monkey-patching z3c.template to use z3c.pt")
    template.ViewPageTemplateFile = _VPT
