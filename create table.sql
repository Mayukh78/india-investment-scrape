create table posts(id serial not null primary key,
post_id varchar(50) unique not null,
created_utc timestamp not null);

create table comments(id serial not null primary key,
post_id varchar(50) not null,
comment_id varchar(50) unique not null,
parent_comment_id varchar(50) not null,
comment_body text not null);