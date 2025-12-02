#!/bin/sh

if [ $# -ne 2 ]; then
	echo "Usage: save-table.sh TABLE FILE" >&2
	exit 1
fi

source .env
docker compose exec postgres /bin/sh -c "pg_dump -U $POSTGRES_USER -d $POSTGRES_DB --table public.$1" > "$2"
