import pytz
from datetime import datetime

def convert_to_utc(time_str, timezone_str):
    try:
        # Create a datetime object with the provided time string
        time_format = "%H:%M:%S"
        input_time = datetime.strptime(time_str, time_format)

        # Get the timezone object corresponding to the provided timezone string
        input_timezone = pytz.timezone(timezone_str)

        # Localize the input time to the provided timezone
        localized_time = input_timezone.localize(input_time, is_dst=None)

        # Convert the localized time to UTC
        utc_time = localized_time.astimezone(pytz.utc)

        # Format the UTC time as a string
        utc_time_str = utc_time.strftime(time_format)

        return utc_time_str
    except ValueError as e:
        return str(e)

# # Example usage:
# input_time_str = "00:10:00"
# input_timezone_str = "America/Chicago"
# utc_time_str = convert_to_utc(input_time_str, input_timezone_str)
# print(f"UTC time: {utc_time_str}")
