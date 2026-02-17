#!/usr/bin/env bash
set -euo pipefail

# Start backend.
(
  case "${OS:-$(uname -s)}" in
    Darwin*) source ".venv/bin/activate" ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT*) source ".venv/Scripts/activate" ;;
    *) source ".venv/bin/activate" ;;
  esac
  python main.py
) &
backend_pid=$!

# Start frontend.
(
  cd agent-ui
  npm run dev
) &
frontend_pid=$!

cleanup() {
  kill "$backend_pid" "$frontend_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

wait "$backend_pid" "$frontend_pid"
