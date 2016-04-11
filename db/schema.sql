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

drop table if exists chord_dept_viz;
create table chord_dept_viz (
    id integer primary key autoincrement,
    deptid text not null,
    facultykey text not null,
    facultydata text not null,
    FOREIGN KEY(deptid) REFERENCES department(rabid)
);

drop table if exists chord_fac_viz;
create table chord_fac_viz (
    id integer primary key autoincrement,
    facid text not null,
    coauthkey text not null,
    coauthdata text not null,
    FOREIGN KEY(facid) REFERENCES faculty(rabid)
);


drop table if exists force_fac_viz;
create table force_fac_viz (
    id integer primary key autoincrement,
    facid text not null,
    nodeuris text not null,
    links text not null,
    FOREIGN KEY(facid) REFERENCES faculty(rabid)
);

drop table if exists force_dept_viz;
create table force_dept_viz (
    id integer primary key autoincrement,
    deptid text not null,
    nodeuris text not null,
    links text not null,
    FOREIGN KEY(deptid) REFERENCES department(rabid)
);