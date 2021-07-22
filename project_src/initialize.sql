create database Excelsior;
use Excelsior;
create table Users(
            Id int auto_increment primary key,
            username varchar(255) not null,
            password varchar(255) not null,
            admin boolean default false not null,
            muted boolean default false not null
        );
insert into Users (username, password, admin)values ('admin', '2B4D48F1-AB5A-4C01-99A6-25480A5BD4E3', 1);
insert into Users (username, password, admin)values ('sample_user', '123456abc', 0);

create table Posts(
    Id int auto_increment primary key,
    thread_id int not null,
    topic_id int not null,
    subject varchar(255) not null,
    body text not null,
    created_at timestamp default current_timestamp not null
);
# Add deleted column to represent removed page
alter table Posts add column deleted boolean default false not null;

#sample page http://localhost:8001/forum?thread_id=0
insert into Posts(subject, topic_id, body, thread_id) values('FOR TEST! DO NOT CLICK', 0, '# DO NOT CLICK', 0);


# add user id in table Posts
alter table Posts add column user_id int not null default 0;