from django.contrib import admin

from vendorprofile.models import *


class VendorProfileAttachmentAdmin(admin.StackedInline):
    model = VendorProfileAttachments


class VendorProfileImagesAdmin(admin.StackedInline):
    model = VendorProfileImages


class VendorProfileVideosAdmin(admin.StackedInline):
    model = VendorProfileVideos


class VendorProfileAdmin(admin.ModelAdmin):
    inlines = [VendorProfileAttachmentAdmin, VendorProfileImagesAdmin, VendorProfileVideosAdmin]


class BusinessSubCategoryPostAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'updated_by')
    list_display = ('business_sub_category', 'business_sub_category_icon', 'business_category', 'created_by', 'created_at', 'updated_by', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
        obj.save()


admin.site.register(BusinessSubCategory, BusinessSubCategoryPostAdmin)

admin.site.register(VendorProfile, VendorProfileAdmin)
admin.site.register(BusinessCategory)
# admin.site.register(BusinessSubCategory)
admin.site.register(VendorCountry)
admin.site.register(VendorCity)


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Facility, FacilityAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Service, ServiceAdmin)
