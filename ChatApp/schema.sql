drop TABLE if EXISTS book_club;
create table book_club(
    book_club_id integer not null auto_increment,
    name varchar(255) not null,
    primary key(book_club_id)
);

drop table if exists book;
create table book(
    book_id integer not null auto_increment,
    title varchar(255) not null,
    author varchar(255) not null,
    isbn varchar(30) not null,
    category varchar(255) not null,
    review text not null,
    primary key(book_id)
);

drop table if exists user;
create table user(
    email varchar(320) not null,
    first_name varchar(20) not null,
    last_name varchar(20) not null,
    username varchar(30) not null,
    password varchar(255) not null,
    primary key (email)
);

drop table if exists post;
create table post(
    post_id integer not null auto_increment,
    title varchar(255) not null,
    text text not null,
    book_club_id INTEGER,
    email varchar(320),
    primary key(post_id),
    FOREIGN KEY (book_club_id)
        REFERENCES book_club(book_club_id),
    FOREIGN KEY (email)
        REFERENCES user(email)
);

drop table if exists book_club_user;
create table book_club_user(
    id integer not null auto_increment,
    book_club_id integer,
    email varchar(320),
    primary key(id),
    foreign key(book_club_id)
    references book_club(book_club_id),
    foreign key(email)
    references user(email)
);

drop table if exists book_club_book;
create table book_club_book(
    id integer not null auto_increment,
    book_club_id integer,
    book_id integer,
    primary key(id),
    foreign key(book_club_id)
    references book_club(book_club_id),
    foreign key(book_id)
    references book(book_id)
);

drop table if exists admin;
create table admin (
    admin_id int not null auto_increment,
    email varchar(320),
    book_club_id integer,
    primary key (admin_id),
    foreign key (email)
        references user(email),
    foreign key (book_club_id)
        references book_club(book_club_id)
);

drop table if exists book_club_join_request;
create table book_club_join_request(
    request_id integer not null auto_increment,
    book_club_id integer,
    admin_id int,
    email varchar(320),
    request_msg text not null,
    primary key (request_id),
    foreign key (book_club_id)
        references book_club(book_club_id),
    foreign key (admin_id)
        references admin(admin_id),
    foreign key (email)
        references user(email)
);