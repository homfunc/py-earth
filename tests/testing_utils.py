import os
import sys
from functools import wraps

import numpy as np
import pytest

try:
    from packaging.version import Version
except ImportError:  # pragma: no cover - fallback for older environments
    from distutils.version import LooseVersion as Version

def if_environ_has(var_name):
    # Test decorator that skips test if environment variable is not defined
    def if_environ(func):
        @wraps(func)
        def run_test(*args, **kwargs):
            if var_name in os.environ:
                return func(*args, **kwargs)
            else:
                pytest.skip(
                    'Only run if %s environment variable is defined.' % var_name
                )
        return run_test
    return if_environ

def if_platform_not_win_32(func):
    @wraps(func)
    def run_test(*args, **kwargs):
        if sys.platform == 'win32':
            pytest.skip('Skip for 32 bit Windows platforms.')
        else:
            return func(*args, **kwargs)
    return run_test
            
def if_sklearn_version_greater_than_or_equal_to(min_version):
    '''
    Test decorator that skips test unless sklearn version is greater than or
    equal to min_version.
    '''
    def _if_sklearn_version(func):
        @wraps(func)
        def run_test(*args, **kwargs):
            import sklearn
            if Version(sklearn.__version__) < Version(min_version):
                pytest.skip('sklearn version less than %s' % str(min_version))
            else:
                return func(*args, **kwargs)
        return run_test
    return _if_sklearn_version


def if_statsmodels(func):
    """Test decorator that skips test if statsmodels not installed. """

    @wraps(func)
    def run_test(*args, **kwargs):
        pytest.importorskip("statsmodels")
        return func(*args, **kwargs)
    return run_test


def if_pandas(func):
    """Test decorator that skips test if pandas not installed. """

    @wraps(func)
    def run_test(*args, **kwargs):
        pytest.importorskip("pandas")
        return func(*args, **kwargs)
    return run_test

def if_sympy(func):
    """ Test decorator that skips test if sympy not installed """ 
    
    @wraps(func)
    def run_test(*args, **kwargs):
        pytest.importorskip("sympy")
        return func(*args, **kwargs)
    return run_test
    


def if_patsy(func):
    """Test decorator that skips test if patsy not installed. """

    @wraps(func)
    def run_test(*args, **kwargs):
        pytest.importorskip("patsy")
        return func(*args, **kwargs)
    return run_test


def assert_list_almost_equal(list1, list2):
    for el1, el2 in zip(list1, list2):
        np.testing.assert_allclose(el1, el2)


def assert_list_almost_equal_value(list, value):
    for el in list:
        np.testing.assert_allclose(el, value)
