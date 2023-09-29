from django.contrib import admin
from data.models import Restaurants, Status, TimeSlice
from report_gen.models import ReportGen

admin.site.register(Restaurants)
admin.site.register(Status)
admin.site.register(TimeSlice)
admin.site.register(ReportGen)

