from django.contrib import admin
from .models import *

class TasklistAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Tasklist, TasklistAdmin)


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ( 'tasklist', 'title', 'start_date', 'end_date', 'status', 'complete', 'customer', 'details')

admin.site.register(Checklist, ChecklistAdmin)