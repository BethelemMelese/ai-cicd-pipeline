import sys
import os
import pytest

# Ensure root path is added
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.operations import add

def test_add_basic():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-2, -3) == -5

def test_add_large_numbers():
    assert add(1e6, 1e6) == 2e6
