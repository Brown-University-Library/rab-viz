drop table if exists faculty;
    create table faculty (
    rabid text primary key,
    shortid text not null,
    firstname text not null,
    lastname text not null,
    preftitle text not null,    
    email text not null
);

drop table if exists visualizations;
    create table visualizations (
    id integer primary key autoincrement,
    vizjson text not null,
);

drop table if exists facultyVizAssoc;
    create table facultyVizAssoc (
    id integer primary key autoincrement,
    facid integer not null,
    vizid integer not null,
    FOREIGN KEY(facid) REFERENCES faculty(rabid),
    FOREIGN KEY(vizid) REFERENCES visualizations(id),
);