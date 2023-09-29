import datetime
import pytz
def utc_local_between(local_start,local_end,local_tz,utc_time):
    # print(local_start)
    # print(local_end)
    # print(utc_time)
    try:
        local_start = datetime.datetime.strptime(local_start,"%H:%M")
    except:
        local_start = datetime.datetime.strptime(local_start,"%H:%M:%S")
    try:
        local_end = datetime.datetime.strptime(local_end,"%H:%M")
    except:
        local_end = datetime.datetime.strptime(local_end,"%H:%M:%S")
    local_tz = pytz.timezone(local_tz)
    local_start = local_tz.localize(local_start, is_dst=None)
    local_end = local_tz.localize(local_end, is_dst=None)
    utc_time = utc_time.strftime("%H:%M:%S")
    utc_time = datetime.datetime.strptime(utc_time,"%H:%M:%S")
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    return local_start <= utc_time <= local_end


