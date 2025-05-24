from flask import Flask, session, render_template, request
import swimclub
from db_utils import db_cm


app = Flask(__name__)
app.secret_key = "secret_key_placeholder"


@app.get("/")
def index():
    return render_template("index.html", title="Welcome to the Swimclub system")


@app.get("/swims")
def get_sessions():
    swim_sessions = db_cm.get_swim_sessions()
    sessions_cleaned = [date[0].split(" ")[0] for date in swim_sessions]
    return render_template(
        "select.html",
        title="Sessions",
        url="/swimmers",
        select_id="swim_session",
        data=sessions_cleaned,
    )


@app.post("/swimmers")
def swimmers_list():
    session["date"] = request.form["swim_session"]
    swimmers = db_cm.get_session_swimmers(session["date"])
    swimmers_cleaned = [f"{name}-{age}" for (name, age) in swimmers]
    return render_template(
        "select.html",
        title="Choose swimmer",
        url="/events",
        select_id="swimmer",
        data=sorted(swimmers_cleaned),
    )


@app.post("/events")
def get_swimmers_files():
    swimmer = request.form["swimmer"]
    session["name"], session["age"] = swimmer.split("-")
    events = db_cm.swimmer_events_by_date(session["name"], session["age"], session["date"])
    events_cleaned = [f"{distance}-{stroke}" for (distance, stroke) in events]
    return render_template(
        "select.html",
        title=f"Choose event for {session['name']}-{session['age']} on {session['date']}",
        url="/chart",
        select_id="event",
        data=events_cleaned,
    )


@app.post("/chart")
def show_bar_chart():
    event = request.form["event"]
    distance, stroke = event.split("-")
    times_array, times_converted, average = (
        swimclub.read_swim_data(session["name"], session["age"], distance, stroke, session["date"])
    )
    record_times = swimclub.get_event_records(distance, stroke)
    times_normalized = swimclub.normalize_times_converted(times_converted, 350)
    title = f"{session['name']} {session['age']} {distance} {stroke} {session['date']}"
    times_zip = zip(reversed(times_normalized), reversed(times_array))
    return render_template(
        "chart.html",
        title=title,
        times_zip=times_zip,
        average=average,
        record_times=record_times,
    )


if __name__ == "__main__":
    app.run()
