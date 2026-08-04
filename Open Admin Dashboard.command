#!/bin/bash
# Double-click to start the B2B2 site + leads backend and open the dashboard.
cd "$(dirname "$0")"
if ! lsof -i :8742 >/dev/null 2>&1; then
  nohup node server/server.js > /tmp/b2b2-server.log 2>&1 &
  sleep 1
fi
open "http://localhost:8742/admin"
echo "B2B2 admin is running at http://localhost:8742/admin (password 0000)."
echo "You can close this window — the server keeps running."
