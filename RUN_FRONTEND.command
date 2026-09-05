#!/bin/zsh
set -e
cd "$(dirname "$0")"
echo ""
echo "🔵 PayRecover AI — FRONTEND / DASHBOARD"
echo "Folder: $(pwd)"
echo ""
if [ ! -d ".venv" ]; then
  echo "Creating Python environment..."
  python3 -m venv .venv
fi
source .venv/bin/activate
if ! python -c "import streamlit" >/dev/null 2>&1; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi
echo ""
echo "Opening PayRecover AI at http://localhost:8501"
python -m streamlit run dashboard.py
