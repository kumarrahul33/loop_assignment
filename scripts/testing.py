from datetime import datetime, timedelta

current_time = datetime.now()
current_time = current_time.replace(minute=0, second=0, microsecond=0)
start_time = current_time - timedelta(weeks=1)
date_time_format = '%Y-%m-%d %H:%M'
while start_time < current_time:
    print(start_time.strftime(date_time_format))
    start_time += timedelta(hours=1)
