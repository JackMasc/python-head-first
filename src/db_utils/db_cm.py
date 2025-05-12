import DBcm
from db_utils import queries

db_details = "SwimDB.sqlite3"


def get_swim_sessions():
    with DBcm.UseDatabase(db_details) as db:
        db.execute(queries.SQL_SESSIONS)
        result = db.fetchall()
    return result


def get_session_swimmers(date):
    with DBcm.UseDatabase(db_details) as db:
        db.execute(queries.SQL_SWIMMERS_BY_SESSION, (date,))
        result = db.fetchall()
    return result


def swimmer_events_by_date(name, age, date):
    with DBcm.UseDatabase(db_details) as db:
        db.execute(queries.SQL_SWIMMERS_EVENTS_BY_SESSION, (name, age, date))
        result = db.fetchall()
    return result


def get_swimmer_times(name, age, distance, stroke, date):
    with DBcm.UseDatabase(db_details) as db:
        db.execute(
            queries.SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
            (name, age, distance, stroke, date),
        )
        result = db.fetchall()
    return result
