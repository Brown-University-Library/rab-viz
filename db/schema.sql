drop table if exists faculty;
create table faculty (
    rabid text primary key,
    lastname text not null,
    firstname text not null,
    fullname text not null,
    abbrev text not null,
    title text not null,    
    deptLabel text not null
);

drop table if exists departments;
create table departments (
    rabid text primary key,
    label text not null,
    useFor text not null
);

drop table if exists affiliations;
create table affiliations (
    id integer primary key autoincrement,
    facid text not null,
    deptid text not null,
    rank integer not null,
    FOREIGN KEY(facid) REFERENCES faculty(rabid),
    FOREIGN KEY(deptid) REFERENCES department(rabid)
);

drop table if exists coauthors;
create table coauthors (
    id integer primary key autoincrement,
    authid text not null,
    coauthid text not null,
    cnt integer not null,
    FOREIGN KEY(authid) REFERENCES faculty(rabid),
    FOREIGN KEY(coauthid) REFERENCES faculty(rabid)
);

drop table if exists author_json;
create table author_json (
    id integer primary key autoincrement,
    facid text not null,
    jsondata text not null,
    FOREIGN KEY(facid) REFERENCES faculty(rabid)
);

drop table if exists chord_viz;
create table chord_viz (
    id integer primary key autoincrement,
    rabid text not null,
    legend text not null,
    matrix text not null
);