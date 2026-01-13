#!/usr/bin/env bash
set -euo pipefail

# Always run from repo root
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Activate conda env hkconnect
CONDA_ACTIVATE="/opt/miniconda3/bin/activate"
if [[ ! -f "$CONDA_ACTIVATE" ]]; then
  echo "ERROR: conda activate script not found at $CONDA_ACTIVATE"
  echo "Edit scripts/enter.sh to match your conda path."
  exit 1
fi

# shellcheck disable=SC1090
source "$CONDA_ACTIVATE" hkconnect

echo "Activated env: hkconnect"
echo "python: $(which python)"
echo "dvc:    $(which dvc || true)"
echo "repo:   $(pwd)"
