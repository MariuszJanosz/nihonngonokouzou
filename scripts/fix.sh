#!/bin/sh

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "==>Activating python venv..."
. ${REPO_ROOT}/.venv/bin/activate

echo "==>Running ruff linting fix..."
ruff check --fix ${REPO_ROOT}

echo "==>Running ruff formatting fix..."
ruff format ${REPO_ROOT}

echo "==>All fixes applied successfully!"
