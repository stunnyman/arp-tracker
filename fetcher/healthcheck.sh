#!/bin/sh
PGUSER=$PG_USER
PGDATABASE=$PG_DB
PGHOST=db

if ! pgrep -f 'fetcher'; then
  echo "ERROR: Fetcher service is not running"
  exit 1
fi

if ! pg_isready -h $PGHOST -U $PGUSER -d $PGDATABASE; then
  echo "ERROR: Cant connect to database"
  exit 1
fi

exit 0