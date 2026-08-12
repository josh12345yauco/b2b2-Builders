#!/bin/bash
# Double-click to start the B2B2 site + leads backend and open the dashboard.
cd "$(dirname "$0")"

# If something other than our Node server holds the port (e.g. the old
# Python preview server), clear it first.
PIDS=$(lsof -ti :8742 -sTCP:LISTEN 2>/dev/null)
if [ -n "$PIDS" ]; then
  for pid in $PIDS; do
    if ! ps -p "$pid" -o comm= | grep -qi node; then
      kill "$pid" 2>/dev/null
    fi
  done
  sleep 1
fi

if ! lsof -ti :8742 -sTCP:LISTEN >/dev/null 2>&1; then
  nohup node server/server.js > /tmp/b2b2-server.log 2>&1 &
  sleep 1
fi

open "http://localhost:8742/admin"
echo "B2B2 admin is running at http://localhost:8742/admin (password 0000)."
echo "You can close this window — the server keeps running."
