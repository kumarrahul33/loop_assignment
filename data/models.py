from django.db import models

def get_default_schedule():
    return {
            "0":{"open": "00:00", "close": "23:59"},  # Sunday
            "1":{"open": "00:00", "close": "23:59"},  # Monday
            "2":{"open": "00:00", "close": "23:59"},  # Tuesday
            "3":{"open": "00:00", "close": "23:59"},  # Wednesday
            "4":{"open": "00:00", "close": "23:59"},  # Thursday
            "5":{"open": "00:00", "close": "23:59"},  # Friday
            "6":{"open": "00:00", "close": "23:59"},  # Saturday
            }

# Create your models here.
## create a model for the time slices
class TimeSlice(models.Model):
    timestamp = models.DateTimeField(unique=True)

    def __str__(self):
        return str(self.timestamp)
    
## create a model for the Restaurants with the following fields
# 1. StoreID : primary key
# 2. open_time and close_time
# 3. original TimeFormat
# 4. timezone : default = America/Chicago

class Restaurants(models.Model):
    storeID = models.IntegerField(unique=True)
    schedule = models.JSONField(default=get_default_schedule) 
    timezone = models.CharField(max_length=100, default='America/Chicago')

    def __str__(self):
        return str(self.storeID)

## create a model with the following fileds
# 1. storeID foreign key
# 2. timeSlice foreign key
# 3. status default = unknown 

class Status(models.Model):
    store = models.ForeignKey(Restaurants, on_delete=models.PROTECT)
    timeSlice = models.ForeignKey(TimeSlice, on_delete=models.PROTECT)
    status = models.CharField(max_length=100, default='unknown')
    extrapolated = models.BooleanField(default=True)
    def __str__(self):
        return str(self.store) + ' ' + str(self.timeSlice) + ' ' + str(self.status)
