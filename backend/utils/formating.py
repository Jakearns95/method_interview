from datetime import datetime


def convert_to_iso8601(dob: str) -> str:
    # Parse the date
    date_obj = datetime.strptime(dob, "%m-%d-%Y")

    # Return the date in ISO 8601 format

    return date_obj.isoformat().split("T")[0]
