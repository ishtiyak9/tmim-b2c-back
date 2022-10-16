import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import *
from django.contrib.admin import SimpleListFilter, FieldListFilter

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

class CustomerFilter(SimpleListFilter, FieldListFilter):
    title = 'customer'
    parameter_name = 'customer'

    def lookups(self, request, model_admin):
        customers = []
        qs = User.objects.filter(user_type='customer')
        for c in qs:
            customers.append([c.id, c.first_name, c.last_name])
        return customers

    def queryset(self, request, queryset):
        if self.value():
            return User.objects.filter(user_type='customer')
        else:
            return queryset


# Register your models here.
class RFQAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('rfq_code', 'customer', 'vendor', 'date')
    list_filter = ['customer', 'vendor', 'date', 'status']
    actions = ["export_as_csv"]
admin.site.register(RFQ, RFQAdmin)

# class QuotationDetailsAdmin(admin.ModelAdmin):
#     list_display = ('message',)
# admin.site.register(QuotationDetails, QuotationDetailsAdmin)