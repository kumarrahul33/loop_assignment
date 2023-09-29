from django.shortcuts import render
from datetime import datetime, timedelta
import random
from threading import Thread
from rest_framework.views import APIView 
from rest_framework import status 
from rest_framework.response import Response
from data.models import Restaurants, Status, TimeSlice
from report_gen.models import ReportGen
import threading

class TriggerReport(APIView):
    def __init__(self):
        self.current_time = datetime.strptime("2023-01-25 18:12:22.323869 UTC", "%Y-%m-%d %H:%M:%S.%f %Z")
        self.report_id = None
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
        self.report_generated = False
        
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
        relevant_time_slices = TimeSlice.objects.filter(timestamp__gte=self.current_time-timedelta(hours=hour,days=day,weeks=week))
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
        # TODO: current time should be the system current time 
        # but for test we are keeping it as the max time of the entries in the status table
        current_time = self.current_time
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
        # TODO: current time should be the system current time 
        # but for test we are keeping it as the max time of the entries in the status table
        # curr_time = datetime.now()
        curr_time = self.current_time
        curr_time = datetime.strptime("2023-01-25 18:12:22.323869 UTC", "%Y-%m-%d %H:%M:%S.%f %Z")
        curr_time = curr_time.replace(minute=0, second=0, microsecond=0)

        # populate the fianl report 
        # iterate throught the relevant time slices and all the the status objects pointing to it and update respective store id entry in the final report

        # for last hour
        self.get_up_down(1,0,0,"uptime_last_hour","downtime_last_hour")
        # for last day
        self.get_up_down(0,1,0,"uptime_last_day","downtime_last_day")
        # for last week 
        self.get_up_down(0,0,1,"uptime_last_week","downtime_last_week")

        report_obj = ReportGen.objects.get(reportID=self.report_id)
        report_obj.report = self.final_report
        report_obj.status = True 
        report_obj.save()
    
    def generate_report(self):
        self.clean_data()
        self.generate_data()
        self.report_generated = True


        
    def get(self,request):
        self.report_id = random.randint(1,1e12)
        report_obj = ReportGen(reportID=self.report_id,status=False,report=self.final_report)
        report_obj.save()
        report_id_data = {
            "report_id": self.report_id
        }
        tc = Thread(target=self.generate_report)
        tc.start()
        return Response(report_id_data, status=status.HTTP_200_OK)

# make an api wihich takes in a report id and returns the report
class GetReport(APIView):
    def __init__(self):
        self.report_id = None
        self.report = None
        self.report_generated = False

    def get(self,request):
        try:
            self.report_id = request.query_params.get('report_id')
            print("report id", self.report_id)
            report_obj = ReportGen.objects.get(reportID=self.report_id)
            if(report_obj.status):
                return Response(report_obj.report, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Report not yet generated"}, status=status.HTTP_400_BAD_REQUEST)
        except ReportGen.DoesNotExist :
            # print()
            dne_response = {"error": "Report Does Not Exist"}
            return Response(dne_response, status=status.HTTP_400_BAD_REQUEST)
        except:
            error_response = {"error": "Internal Server Error"} 
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


