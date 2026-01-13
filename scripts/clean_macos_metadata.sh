#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

find . -name '._*' -type f -delete || true
find . -name '.__*' -type f -delete || true
find . -name '.DS_Store' -type f -delete || true

echo "Cleaned macOS metadata files."
