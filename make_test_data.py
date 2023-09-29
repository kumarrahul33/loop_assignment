import pandas as pd


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

get_max_time()