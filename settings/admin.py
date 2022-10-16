from django.contrib import admin
from settings.models import Brand, Unit, Color, Vat, Commission

# Register your models here.
class VatAdmin(admin.ModelAdmin):
    list_display = ('percentage',)

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

class ComissionAdmin(admin.ModelAdmin):
    list_display = ('percentage',)

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
admin.site.register(Brand)
admin.site.register(Unit)
admin.site.register(Color)
admin.site.register(Vat,VatAdmin)
admin.site.register(Commission,ComissionAdmin)