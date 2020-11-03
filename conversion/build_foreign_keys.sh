#!/bin/sh

source ./config.sh

$OUT_DB_PSQL << _EOF_
alter table parent_child add foreign key (parent_id) references files(id);
alter table parent_child add foreign key (child_id) references files(id);

alter table files add foreign key(creator)      references users(username);
alter table files add foreign key(namespace)    references namespaces(name);

alter table files_datasets add foreign key (dataset_namespace, dataset_name) 
        references datasets(namespace, name) 
        on delete cascade;
alter table files_datasets add foreign key (file_id) 
        references files(id) 
        on delete cascade;

alter table parameter_categories add foreign key (owner) references users(username);
alter table parameter_categories add foreign key (creator) references users(username);

_EOF_

