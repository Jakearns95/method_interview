from datetime import datetime
import csv
from io import StringIO
from typing import List, Dict


def convert_to_iso8601(dob: str) -> str:
    # Parse the date
    date_obj = datetime.strptime(dob, "%m-%d-%Y")

    # Return the date in ISO 8601 format

    return date_obj.isoformat().split("T")[0]


def convert_to_csv(data_list: List[Dict]) -> StringIO:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data_list[0].keys())
    writer.writeheader()
    writer.writerows(data_list)
    return output
