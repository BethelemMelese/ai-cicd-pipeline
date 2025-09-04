import sys
import os
import pytest

# Ensure root path is added
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.operations import subtract

def test_subtract_basic():
    assert subtract(5, 3) == 2

def test_subtract_negative():
    assert subtract(-5, -3) == -2

def test_subtract_large_numbers():
    assert subtract(1e6, 1e5) == 9e5
