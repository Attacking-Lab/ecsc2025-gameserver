#!/bin/sh

docker compose exec -i -T cp /bin/sh <<EOF
uv run scripts/sync_teams_http.py
EOF
