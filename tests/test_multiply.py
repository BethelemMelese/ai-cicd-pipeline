import sys
import os
import pytest

# Ensure root path is added
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.operations import multiply

def test_multiply_basic():
    assert multiply(3, 4) == 12

def test_multiply_by_zero():
    assert multiply(5, 0) == 0

def test_multiply_large_numbers():
    assert multiply(1e3, 1e3) == 1e6
