import csv
from django.contrib import admin
from django.http import HttpResponse
from datetime import date

from guest.models import *

# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     writer = csv.writer(response)
#     writer.writerow(['name', 'relationship', 'phone', 'email'])

#     for guest in Guest.objects.all().values_list('name', 'relationship', 'phone', 'email'):
#         writer.writerow(guest)
    
#     response['Content-Disposition'] = "attachment; filename='members.csv'"

#     return response

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class GuestAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name','relationship','phone', 'email',)
    list_filter = ('relationship', 'created_by', 'invitation_date',)
    actions = ["export_as_csv"]

admin.site.register(Guest, GuestAdmin)

class GuestlandingAdmin(admin.ModelAdmin):
    list_display = ('host', 'image', 'details', 'address', 'date')

admin.site.register(Guestlanding, GuestlandingAdmin)
admin.site.register(OccasionType)

