#!/bin/bash
set -uo pipefail
set +e

FAILURE=false

echo "safety"
safety check -r requirements.txt -r requirements-dev.txt || FAILURE=true

echo "pylint"
pylint squat_recognizer training  || FAILURE=true

echo "pycodestyle"
pycodestyle squat_recognizer training  || FAILURE=true

echo "mypy"
mypy  squat_recognizer training  || FAILURE=true

echo "bandit"
bandit -11 -r {squat_recognizer, training}  || FAILURE=true

echo "shellcheck"
shellcheck tasks/*.sh || FAILURE=true

if [ "$FAILURE" = true]; then 
  echo "Linting failed"
  exit 1
fi

echo "Linting passed"
exit 0