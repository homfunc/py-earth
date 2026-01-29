import os

import pytest

import pyearth

pyearth_dir = os.path.dirname(os.path.abspath(pyearth.__file__))
os.chdir(pyearth_dir)
raise SystemExit(pytest.main(["-q"]))
