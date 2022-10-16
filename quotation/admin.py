import csv
from django.contrib import admin
from django.http import HttpResponse
from quotation.models import *

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

# Register your models here.
class QuotationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('quotation_code', 'vendor', 'customer', 'date')
    list_filter = ['vendor', 'customer', 'date', 'status']
    actions = ["export_as_csv"]

admin.site.register(Quotation, QuotationAdmin)