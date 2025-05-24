SQL_SESSIONS = """
    select distinct ts from times;
"""

SQL_SWIMMERS_BY_SESSION = """
    select distinct swimmers.name, swimmers.age
    from swimmers
    join times on times.swimmer_id = swimmers.id
    where date(times.ts) = ?
    order by swimmers.name;
"""

SQL_SWIMMERS_EVENTS_BY_SESSION = """
    select distinct events.distance, events.stroke
    from swimmers, events, times
    where
    swimmers.name = ? and
    swimmers.age = ? and
    date(times.ts) = ? and
    times.swimmer_id = swimmers.id and
    times.event_id = events.id
"""

SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION = """
    select times.time
    from times, swimmers, events
    where
    swimmers.name = ? and
    swimmers.age = ? and
    events.distance = ? and
    events.stroke = ? and
    date(times.ts) = ? and
    times.swimmer_id = swimmers.id and
    times.event_id = events.id
"""
