#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

from ggplot import aes
from ggplot import xlab
from ggplot import ylab
from ggplot import ggplot
from ggplot import geom_density

import numpy as np
import pandas as pd

from PIL import Image as PLTImage

from nti.analytics_pandas.utils.save_plot import save_plot_to_png

def _build_testing_plot():
    df = pd.DataFrame({
        "x": np.arange(0, 100),
        "y": np.arange(0, 100),
        "z": np.arange(0, 100)
    })

    df['y'] = np.sin(df.y)
    df['z'] = df['y'] + 100
    df['c'] = np.where(df.x%2==0,"red", "blue")

    plot = ggplot(aes(x="x", color="c"), data=df)
    plot = plot + geom_density() + xlab("x label") + ylab("y label")
    return plot

class TestSavePlot(AnalyticsPandasTestBase):
	def test_save_plot(self):
		plot =  _build_testing_plot()
		image_filename = 'image_test.png'
		image = save_plot_to_png(plot, image_filename)
		image.data.seek(0)
		im = PLTImage.open(image.data)
		im.show()