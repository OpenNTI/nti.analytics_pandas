#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from io import BytesIO

logger = __import__('logging').getLogger(__name__)


class Image(object):

    @classmethod
    def process(cls, filename, data):
        # pylint: disable=attribute-defined-outside-init
        me = cls()
        me.filename = filename
        me.data = data
        return me


class Plot(object):

    @classmethod
    def process(cls, plot_name, plot):
        # pylint: disable=attribute-defined-outside-init
        me = cls()
        me.plot_name = plot_name
        me.plot = plot
        return me


def save_plot_(plot, image_filename, image_type='png'):
    """
    ega: please keep this function for further reference
    """
    buf = BytesIO()
    plot.save(image_filename)
    image_filename = u'%s.%s' % (image_filename, image_type)
    image = Image.process(image_filename, buf)
    return image
save_plot = save_plot_
