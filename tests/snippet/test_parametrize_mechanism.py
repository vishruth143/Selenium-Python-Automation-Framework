# pylint: disable=[missing-module-docstring, missing-function-docstring]

import pytest

@pytest.mark.param
@pytest.mark.parametrize("num", [2, 4, 5])
def test_is_even(num):
    assert num % 2 == 0
