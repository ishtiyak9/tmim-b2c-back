import csv
from user.models import City, User, Country 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from user.forms import CustomUserChangeForm, CustomUserCreationForm


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
class UsersAdmin(UserAdmin, ExportCsvMixin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Profile info'), {'fields': ('first_name','last_name','phone','address','dob','image','cover_photo','gender', 'about_me', 'user_type', 'city','country','language')}),
        (_('Permissions'),
         {'fields': ('groups', 'is_active', 'is_approved', 'is_subscribed', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        'email','first_name','last_name', 'user_type',  'is_active', 'is_staff', 'is_approved', 'is_subscribed' 
    )
    list_display_links = ('email',)
    list_filter = ['user_type','groups',  'is_subscribed',]
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    actions = ['export_as_csv']


admin.site.register(User, UsersAdmin)
admin.site.register(Country)
admin.site.register(City)
