import sys
import os
import pytest

# Ensure root path is added
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.operations import divide

def test_divide_basic():
    assert divide(10, 2) == 5

def test_divide_fraction():
    assert divide(3, 2) == 1.5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
