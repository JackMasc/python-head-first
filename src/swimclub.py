import statistics
import json
from db_utils import db_cm


JSON_DATA = "swimdata/records.json"


def read_swim_data(name, age, distance, stroke, date):
    """
    Return swim data from a file.
    """

    times_raw = db_cm.get_swimmer_times(name, age, distance, stroke, date)
    times_array = [time[0] for time in times_raw]

    times_converted = []
    for time in times_array:

        if ":" in time:
            minutes_string, rest = time.split(":")
        else:
            minutes_string = "0"
            rest = time

        if "." in rest:
            seconds_string, hundreds_string = rest.split(".")
        else:
            seconds_string = rest
            hundreds_string = "0"

        time_hundreds = (
            int(minutes_string) * 100 * 60
            + int(seconds_string) * 100
            + int(hundreds_string)
        )

        times_converted.append(time_hundreds)

    times_mean = statistics.mean(times_converted)
    mean_minutes = int(times_mean // 6000)
    mean_seconds = int((times_mean - mean_minutes * 6000) // 100)

    mean_hundreds = int(times_mean - mean_seconds * 100 - mean_minutes * 6000)
    average = f"{mean_minutes:02}:{mean_seconds:02}.{mean_hundreds:02}"

    return times_array, times_converted, average


def get_event_records(distance, stroke):
    conversions = {
        "Free": "freestyle",
        "Back": "backstroke",
        "Breast": "breaststroke",
        "Fly": "butterfly",
        "IM": "individual medley",
    }

    converted_event = f"{distance} {conversions[stroke]}"

    with open(JSON_DATA) as file:
        records: dict[str, dict] = json.load(file)
    COURSES = ("SC Men", "LC Men", "SC Women", "LC Women")
    record_times = []
    for course in COURSES:
        record = records[course].setdefault(converted_event, 'udefined')
        record_times.append(record)
    return record_times


def normalize_times_converted(times_converted, bar_lenght):
    max_time = max(times_converted)
    normalized_times = []
    for time in times_converted:
        normalized_times.append(int(round(time / max_time * bar_lenght, 0)))
    return normalized_times
