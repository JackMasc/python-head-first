import DBcm

DB_DETAILS = "../db_utils/SwimDB.sqlite3"

SQL_SWIMMERS = """
    create table if not exists swimmers(
        id integer not null primary key autoincrement,
        name varchar(32) not null,
        age integer not null
    )
"""

SQL_EVENTS = """
    create table if not exists events(
        id integer not null primary key autoincrement,
        distance varchar(16) not null,
        stroke varchart(16) not null
    )
"""

SQL_TIMES = """
    create table if not exists times(
        swimmer_id integer not null,
        event_id integer not null,
        time varchart(16),
        ts timestamp default current_timestamp
    )
"""

with DBcm.UseDatabase(config=DB_DETAILS) as db:
    db.execute(SQL_SWIMMERS)
    db.execute(SQL_EVENTS)
    db.execute(SQL_TIMES)
    db.execute("pragma table_list")
    result = db.fetchall()
