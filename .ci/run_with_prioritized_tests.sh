#!/usr/bin/env bash
set -euo pipefail

if [[ -s ".ci/prioritized_tests.txt" ]]; then
  echo "Running prioritized tests from .ci/prioritized_tests.txt ..."
  xargs -a .ci/prioritized_tests.txt pytest -q --maxfail=1 --disable-warnings
else
  echo "No prioritized tests found; running full test suite ..."
  pytest -q --maxfail=1 --disable-warnings
fi
