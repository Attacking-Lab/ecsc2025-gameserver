#!/bin/sh

if [ $# -ne 1 ]; then
	echo "Usage: load-table.sh FILE" >&2
	exit 1
fi

source .env
cat "$1" | docker compose exec -T postgres /bin/sh -c "psql -U $POSTGRES_USER -d $POSTGRES_DB -f -"
