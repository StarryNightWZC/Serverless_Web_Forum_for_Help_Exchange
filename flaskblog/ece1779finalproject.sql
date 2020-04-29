create schema if not exists testtable;

use testtable;

drop table if exists post;
create table if not exists post (
  id integer not null auto_increment,
  title varchar(100) not null,
  type varchar(50) not null,
  phone varchar(20) not null,
  emailaddress varchar(120) not null,
  address varchar(120) not null,
  date_posted datetime not null,
  content varchar(1000) not null,
  user_id integer not null,
  primary key (id)
);

 
drop table if exists user;
create table if not exists user (
  id integer not null auto_increment,
  username varchar(20) not null,
  email varchar(120) not null,
  image_file varchar(20) not null,
  password varchar(60) not null,
  primary key (id)
);

