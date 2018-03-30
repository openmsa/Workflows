#!/bin/bash

function usage {
  echo "Usage: $0 [OPTION]..."
  echo "Run nalclient's test suite(s)"
  echo ""
  echo "  -p, --pep8               Just run flake8"
  echo "  -h, --help               Print this usage message"
  echo "  -c, --coverage           Get coverage"
  echo ""
  echo "This script is deprecated and currently retained for compatibility."
  echo 'You can run the full test suite for multiple environments by running "tox".'
  echo 'You can run tests for only python 2.7 by running "tox -e py27", or run only'
  echo 'the flake8 tests with "tox -e pep8".'
  exit
}

command -v tox > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo 'This script requires "tox" to run.'
  echo 'You can install it with "pip install tox".'
  exit 1;
fi

just_pep8=0

function process_option {
  case "$1" in
    -h|--help) usage;;
    -p|--pep8) just_pep8=1;;
    -c|--coverage) just_cover=1;;
  esac
}

for arg in "$@"; do
  process_option $arg
done

if [ $just_pep8 -eq 1 ]; then
  tox -e pep8
  exit
fi

if [ $just_cover -eq 1 ]; then
  tox -e cover
  exit
fi

tox -e py27 2>&1 | tee run_tests.err.log  || exit
if [ ${PIPESTATUS[0]} -ne 0 ]; then
  exit ${PIPESTATUS[0]}
fi

tox -e pep8