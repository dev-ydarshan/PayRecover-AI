#!/bin/zsh
set -e
cd "$(dirname "$0")"
echo ""
echo "🟢 PayRecover AI — BACKEND / PIPELINE"
echo "Folder: $(pwd)"
echo ""
if [ ! -d ".venv" ]; then
  echo "Creating Python environment..."
  python3 -m venv .venv
fi
source .venv/bin/activate
if ! python -c "import streamlit, pandas, supabase" >/dev/null 2>&1; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi
if [ ! -f ".env" ]; then
  echo ""
  echo "⚠️  .env is missing."
  echo "Copy the .env from your already-working PayRecover project into this folder."
  echo "Then run this file again."
  echo ""
  read -k 1 "?Press any key to close..."
  exit 1
fi
echo "Running recovery pipeline..."
python run_pipeline.py
