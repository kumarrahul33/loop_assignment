from data.models import Restaurants
from data.models import TimeSlice
from data.models import Status
import csv
import os
import django
import pytz
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loop.settings')  # Replace 'yourproject' with your project's name
django.setup()

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

def parse_time(time_str,timezone_str):
        time_format = "%H:%M:%S"
        out_time_format = "%H:%M:%S %Z"
        input_time = datetime.strptime(time_str, time_format)

        # Get the timezone object corresponding to the provided timezone string
        input_timezone = pytz.timezone(timezone_str)
        
        # add the timezone to the time object
        input_time = input_timezone.localize(input_time, is_dst=None)
        return input_time.strftime(out_time_format)

def import_timezones():
    csv_file_path = 'dummy_tz.csv' 


    with open(csv_file_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            # print(row['store_id'], row['timezone_str'])
            try:
                store_id = row['store_id']
                timezone = row['timezone_str']
                # create a new restaurant object
                new_restaurant = Restaurants(storeID=store_id,timezone=timezone)
                new_restaurant.save()
            except:
                pass

# takes in the time (t) and the timezone and returns the time in UTC

def import_office_hours():
    csv_file_path = 'dummy_office_hours.csv'
    with open(csv_file_path,'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            store_id = row['store_id']
            try:
                restaurant = Restaurants.objects.get(storeID=store_id)
                st = row['start_time_local']
                et = row['end_time_local']
                day = row['day']
                restaurant.schedule[day] = {'open':st, 'close':et}
                restaurant.save()
            except Exception as e:
                new_restaurant = Restaurants(storeID=store_id,timezone='America/Chicago')
                new_restaurant.save()
                st = row['start_time_local']
                et = row['end_time_local']
                restaurant.schedule[day] = {'open':st, 'close':et}

def get_time_slice_time(time_str):
    time_format = "%Y-%m-%d %H:%M:%S.%f %Z"
    input_time = datetime.strptime(time_str, time_format)

    input_time = input_time.replace(minute=0, second=0, microsecond=0)
    utc_tz = pytz.timezone("UTC")
    input_time = utc_tz.localize(input_time)
    # formatted_utc_time = input_time.strftime("%Y-%m-%d %H:%M %Z")
    formatted_utc_time = input_time.isoformat()
    return formatted_utc_time
               

def import_status():
    csv_file_path = 'dummy_status.csv'
    with open(csv_file_path,'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            store_id = row['store_id']
            restaurant = None
            try:
                restaurant = Restaurants.objects.get(storeID=store_id)
            except:
                print("Restaurant not found:", store_id)
                continue

            curr_time = row['timestamp_utc']
            # print(curr_time)
            curr_time = get_time_slice_time(curr_time)
            # print(curr_time)
            # find the time slice object
            curr_time_slice = None
            try:
                curr_time_slice = TimeSlice.objects.get(timestamp=curr_time)
            except:
                curr_time_slice = TimeSlice(timestamp=curr_time)
                curr_time_slice.save()

            curr_status_obj = None
            try:
                curr_status_obj = Status.objects.get(store=restaurant,timeSlice=curr_time_slice)
            except:
                curr_status_obj = Status(store=restaurant,timeSlice=curr_time_slice)
            
            curr_status_obj.status = row['status']
            curr_status_obj.extrapolated = False 
            curr_status_obj.save()

import_timezones()
import_office_hours()
import_status() 


