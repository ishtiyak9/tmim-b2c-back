import csv
from django.contrib import admin
from django.http import HttpResponse
from subscription.models import *

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


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('subscription_plan', 'fees', )

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)


class SubscriptionAdmin(admin.ModelAdmin, ExportCsvMixin):
    exclude = ['created_by','updated_by']
    list_display = ('vendor', 'payment_status', 'fees', 'created_at')
    actions = ["export_as_csv"]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
            'customer.js',  # app static folder
        )
admin.site.register(Subscription, SubscriptionAdmin)
