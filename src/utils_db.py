import DBcm
import os
from swimclub import DATA_FOLDER


files = os.listdir(DATA_FOLDER)
files.remove(".DS_Store")

db_details = "SwimDB.sqlite3"

SQL_INSERT_SWIMMER = """
    insert into swimmers
    (name, age)
    values
    (?,?)
"""

SQL_SELECT_SWIMMER = """
    select *
    from swimmers
    where name = ? and age = ?;
"""

SQL_INSERT_EVENT = """
    insert into events
    (distance, stroke) 
    values
    (?, ?);
"""

SQL_SELECT_EVENT = """
    select *
    from events
    where distance = ? and stroke = ?;
"""

SQL_GET_EVENT_ID = """
    select id
    from events
    where distance = ? and stroke = ?;
"""

SQL_GET_SWIMMER_ID = """
    select id
    from swimmers
    where name = ? and age = ?;
"""

SQL_INSERT_TIME = """
    insert into times
    (swimmer_id, event_id, time)
    values
    (?,?,?);
"""


with DBcm.UseDatabase(db_details) as db:
    for file_name in files:
        name, age, distance, stroke = file_name.removesuffix(".txt").split("-")

        db.execute(SQL_SELECT_SWIMMER, (name, age))
        result = db.fetchall()
        if not result:  
            db.execute(SQL_INSERT_SWIMMER, (name, age))

        db.execute(SQL_SELECT_EVENT, (distance, stroke))
        result = db.fetchall()
        if not result:
            db.execute(SQL_INSERT_EVENT, (distance, stroke))

        db.execute(SQL_GET_SWIMMER_ID, (name, age))
        result = db.fetchone()
        swimmer_id = result[0]

        db.execute(SQL_GET_EVENT_ID, (distance, stroke))
        result = db.fetchone()
        event_id = result[0]

        with open(DATA_FOLDER + file_name, "r") as file:
            lines = file.readlines()
        times = lines[0].strip().split(",")

        for time in times:
            db.execute(SQL_INSERT_TIME, (swimmer_id, event_id, time))