from django.shortcuts import render
from datetime import datetime, timedelta

# Create your views here.
# using restframework make a view for get request 
from rest_framework.views import APIView 
from rest_framework import status 
from rest_framework.response import Response
from data.models import Restaurants, Status, TimeSlice

class TriggerReport(APIView):
    def __init__(self):
        restaurants = Restaurants.objects.all()
        self.final_report = dict()
        for elem_restaurants in restaurants:
            self.final_report[elem_restaurants.storeID] = {
                    "uptime_last_hour": 0,
                    "uptime_last_day": 0,
                    "uptime_last_week": 0,
                    "downtime_last_hour": 0,
                    "downtime_last_day": 0,
                    "downtime_last_week": 0,
            }
        
    def extrapolation_logic(self, status_obj):
        prev_three_status = Status.objects.filter(storeID=status_obj.storeID,timeSlice__lt=status_obj.timeSlice).order_by('-timeSlice')[:3]
        count_active = 0
        for obj in prev_three_status:
            if(obj.status == 'active'):
                count_active += 1
        if(count_active >= 2):
            return 'active'
        else:
            return 'inactive'

    def in_office_hours(self, status_obj, restaurant_id):
        restaurant_obj = Restaurants.objects.get(storeID=restaurant_id)
        office_hours = restaurant_obj.schedule[status_obj.timeSlice.timestamp.weekday()]
        office_hours_open = office_hours['open']
        office_hours_close = office_hours['close']
        if(office_hours_open <= status_obj.timeSlice.timestamp.strftime("%H:%M") <= office_hours_close):
            return True
        return False

    def get_up_down(self, hour,day,week,up_key, down_key):
        relevant_time_slices = TimeSlice.objects.filter(timestamp__gte=datetime.now()-timedelta(hours=hour,days=day,weeks=week))
        for time_slice in relevant_time_slices: 
            status_objs = Status.objects.filter(timeSlice=time_slice)
            for status_obj in status_objs:
                if(not self.in_office_hours(status_obj, status_obj.storeID)):
                    continue
                if(status_obj.status == 'active'):
                    self.final_report[status_obj.storeID][up_key] += 1 
                else:
                    self.final_report[status_obj.storeID][down_key] += 1

    def clean_data(self):
        current_time = datetime.now()
        current_time = current_time.replace(minute=0, second=0, microsecond=0)
        start_time = current_time - timedelta(weeks=1)
        while start_time < current_time:
            if(TimeSlice.objects.filter(timestamp=start_time).exists()):
                continue
            else:
                new_time_slice = TimeSlice(timestamp=start_time)
                new_time_slice.save()
            start_time += timedelta(hours=1)

        relevant_time_slices = TimeSlice.objects.filter(timestamp__gte=current_time-timedelta(weeks=1))
        # iterate through all the restaurants and generate the status for each time slice if not present and extrapolate the newly created status object 
        restaurants = Restaurants.objects.all()
        for restaurant in restaurants:
            for time_slice in relevant_time_slices:
                if(Status.objects.filter(storeID=restaurant,timeSlice=time_slice).exists()):
                    continue
                else:
                    new_status = Status(storeID=restaurant,timeSlice=time_slice)
                    new_status.save()
                    new_status.extrapolated = True
                    new_status.status = self.extrapolation_logic(new_status)
                    new_status.save()

    def generate_data(self):
        curr_time = datetime.now()
        curr_time = curr_time.replace(minute=0, second=0, microsecond=0)

        # populate the fianl report 
        # iterate throught the relevant time slices and all the the status objects pointing to it and update respective store id entry in the final report

        # for last hour
        self.get_up_down(1,0,0,"uptime_last_hour","downtime_last_hour")
        # for last day
        self.get_up_down(0,1,0,"uptime_last_day","downtime_last_day")
        # for last week 
        self.get_up_down(0,0,1,"uptime_last_week","downtime_last_week")
        
    def get(self,request):
        self.clean_data()
        self.generate_data()
        return Response(self.final_report,status=status.HTTP_200_OK)


