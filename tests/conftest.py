import numpy as np
import pytest

@pytest.fixture
def random_seed():
    np.random.seed(0)

@pytest.fixture
def sample_data(random_seed):
    m = 1000
    n = 10
    X = 80 * np.random.uniform(size=(m, n)) - 40
    y = np.abs(X[:, 6] - 4.0) + 1 * np.random.normal(size=m)
    return X, y
