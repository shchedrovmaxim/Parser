CREATE TABLE DomRia (
    number_of_rooms     INTEGER DEFAULT Null, 
    total_space         REAL DEFAULT Null,
    price               INTEGER DEFAULT Null,
    living_space        REAL DEFAULT Null,
    kitchen_space       REAL DEFAULT Null,
    who_saler           TEXT DEFAULT Null,
    floor               INTEGER DEFAULT Null,
    storeys             INTEGER DEFAULT Null,
    distance_center     TEXT DEFAULT Null,
    type_center         TEXT DEFAULT Null,
    type_heating        TEXT DEFAULT Null,
    distance_subway     TEXT DEFAULT Null,
    type_subway         TEXT DEFAULT Null,
    distance_market     TEXT DEFAULT Null,
    type_market         TEXT DEFAULT Null,
    picture             TEXT[] DEFAULT Null,
    url                 TEXT DEFAULT Null,
   
    addres              TEXT DEFAULT Null,
    uniqueID            INTEGER PRIMARY KEY DEFAULT Null,
    data_of_pulication  TEXT DEFAULT Null,
    description         TEXT DEFAULT Null
);