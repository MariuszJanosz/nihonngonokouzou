#!/bin/sh

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd ${REPO_ROOT}

echo "==>Activating python venv..."
. "${REPO_ROOT}/.venv/bin/activate"

echo "==>Running ruff linting check..."
ruff check "${REPO_ROOT}"

echo "==>Running ruff formatting check..."
ruff format --check "${REPO_ROOT}"

echo "==>Running mypy type check..."
mypy .

echo "==>Running tests..."
"${SCRIPT_DIR}/test.sh"

echo "==>All checks passed!"
