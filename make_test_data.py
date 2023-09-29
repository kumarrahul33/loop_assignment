import pandas as pd
from data.models import Restaurants
from data.models import Status
from datetime import datetime
from data.models import TimeSlice
import pytz


def make_test_data():
    tz = pd.read_csv('dummy_tz.csv')
    office_hours = pd.read_csv("Menu hours.csv")
    status = pd.read_csv("store status.csv")

    # put all the store Id in a list this is the first column of the tz dataframe
    relevant_stores = tz['store_id'].tolist()

    # iterate over the store status and keep the entries with the store id in the relevant_stores list

    status = status[status['store_id'].isin(relevant_stores)]
    office_hours = office_hours[office_hours['store_id'].isin(relevant_stores)]

    status.to_csv('dummy_status.csv', index=False)
    office_hours.to_csv('dummy_office_hours.csv', index=False)

def get_max_time():
    status = pd.read_csv("dummy_status.csv")
    # read the timestamp_utc column and find the max time
    max_time = status['timestamp_utc'].max()
    print(max_time)


def validate_test_data():
    status = pd.read_csv("dummy_status.csv")
    office_hours = pd.read_csv("dummy_office_hours.csv")
    tz = pd.read_csv('dummy_tz.csv')
    
    curr_store = 8445695079583663910 
    restaurant_obj = Restaurants.objects.get(storeID=curr_store)
    print(restaurant_obj.schedule)
    # find the current store in the office hours
    curr_store_office_hours = office_hours[office_hours['store_id'] == curr_store]
    print(curr_store_office_hours)

    # find the current store in the tz
    curr_store_tz = tz[tz['store_id'] == curr_store]
    print(curr_store_tz)


    
    for index,row in status.iterrows():
        if(row['store_id'] == curr_store):
            print("time: ",row['timestamp_utc'], " status: ", row['status']) 
        
# validate_test_data()
