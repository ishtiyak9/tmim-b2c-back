from mptt.admin import DraggableMPTTAdmin
from .models import *
from django.contrib import admin



class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions',
                    'indented_title',
                    # 'related_products_count',
                    # 'related_products_cumulative_count'
                    )
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


admin.site.register(Category, CategoryAdmin)



# class FacilityAdmin(admin.ModelAdmin):
#     list_display = ('name',)
# admin.site.register(Facility, FacilityAdmin)

# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('name',)
# admin.site.register(Service, ServiceAdmin)