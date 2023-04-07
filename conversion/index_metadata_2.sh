#!/bin/sh

source ./config.sh

$OUT_DB_PSQL << _EOF_

create index files_meta_path_ops_index on files using gin (metadata jsonb_path_ops);

_EOF_
