drop table if exists faculty;
create table faculty (
    rabid text primary key,
    shortid text not null,
    firstname text not null,
    lastname text not null,
    fullname text not null,
    nameabbrev text not null,
    preftitle text not null,    
    email text not null,
    primarydept text not null,
    FOREIGN KEY(primarydept) REFERENCES department(rabid)
);

drop table if exists department;
create table department (
    rabid text primary key,
    label text not null
);

drop table if exists chord_department;
create table chord_department (
    id integer primary key autoincrement,
    deptid text not null,
    facultykey text not null,
    facultydata text not null,
    FOREIGN KEY(deptid) REFERENCES department(rabid)
);

drop table if exists chord_faculty;
create table chord_faculty (
    id integer primary key autoincrement,
    facultyid text not null,
    key text not null,
    data text not null,
    FOREIGN KEY(facultyid) REFERENCES faculty(rabid)
);

drop table if exists force_department;
create table force_department (
    id integer primary key autoincrement,
    deptid text not null,
    nodes text not null,
    links text not null,
    FOREIGN KEY(deptid) REFERENCES department(rabid)
);