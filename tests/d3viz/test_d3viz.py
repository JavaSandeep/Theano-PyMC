import filecmp
import os.path as pt
import tempfile

import numpy as np
import pytest

import theano as th
import theano.d3viz as d3v
from tests.d3viz import models
from theano.d3viz.formatting import pydot_imported, pydot_imported_msg


if not pydot_imported:
    pytest.skip("pydot not available: " + pydot_imported_msg, allow_module_level=True)


class TestD3Viz:
    def setup_method(self):
        self.rng = np.random.RandomState(0)
        self.data_dir = pt.join("data", "test_d3viz")

    def check(self, f, reference=None, verbose=False):
        tmp_dir = tempfile.mkdtemp()
        html_file = pt.join(tmp_dir, "index.html")
        if verbose:
            print(html_file)
        d3v.d3viz(f, html_file)
        assert pt.getsize(html_file) > 0
        if reference:
            assert filecmp.cmp(html_file, reference)

    def test_mlp(self):
        m = models.Mlp()
        f = th.function(m.inputs, m.outputs)
        self.check(f)

    def test_mlp_profiled(self):
        if th.config.mode in ("DebugMode", "DEBUG_MODE"):
            pytest.skip("Can't profile in DebugMode")
        m = models.Mlp()
        profile = th.compile.profiling.ProfileStats(False)
        f = th.function(m.inputs, m.outputs, profile=profile)
        x_val = self.rng.normal(0, 1, (1000, m.nfeatures))
        f(x_val)
        self.check(f)

    def test_ofg(self):
        m = models.Ofg()
        f = th.function(m.inputs, m.outputs)
        self.check(f)

    def test_ofg_nested(self):
        m = models.OfgNested()
        f = th.function(m.inputs, m.outputs)
        self.check(f)

    def test_ofg_simple(self):
        m = models.OfgSimple()
        f = th.function(m.inputs, m.outputs)
        self.check(f)
