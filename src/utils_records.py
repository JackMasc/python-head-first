import gazpacho
import json
import pandas as pd


COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
JSON_DATA = "swimdata/records.json"
RECORDS = (0, 2, 4, 5)
URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"


def create_dict_with_gazpacho():
    html = gazpacho.get(URL)
    soup = gazpacho.Soup(html)
    tables = soup.find("table", mode="all")
    records_dict = {}
    for n_table, course in zip(RECORDS, COURSES):
        table = tables[n_table]
        rows = table.find("tr", mode="all")
        records_dict[course] = {}
        for row in rows[1:]:
            columns = row.find("td", mode="all")[0:2]
            event = columns[0].text
            time = columns[1].text
            if "relay" not in event:
                records_dict[course][event] = time

    with open(JSON_DATA, "w") as file:
        json.dump(records_dict, file)


def create_dict_with_pandas():
    tables = pd.read_html(URL)
    records_dict = {}

    for table, course in zip(RECORDS, COURSES):
        df = tables[table][["Event", "Time"]]
        df = df[~df["Event"].str.contains("relay")]
        df = df.set_index("Event")
        records_dict[course] = df.to_dict()["Time"]

    with open(JSON_DATA, "w") as file:
        json.dump(records_dict, file)

def main():
    # Using gazpacho since it's faster
    create_dict_with_gazpacho()

if __name__ == "__main__":
    main()