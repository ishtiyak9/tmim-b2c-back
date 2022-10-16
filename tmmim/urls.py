"""tmmim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from rest_framework.documentation import include_docs_urls

from tmmim import settings

admin.site.site_header = 'Tmmim Admin Dashboard'
admin.site.site_title = 'Tmmim Admin Dashboard'
admin.site.index_title = 'Tmmim Dashboard Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('api/', include('user.urls', namespace='api')),
    path('api/', include('vendorprofile.urls')),
    path('api/', include('requestforquote.urls')),
    path('api/quotation/', include('quotation.urls')),
    path('api/', include('subscription.urls')),
    path('api/guest/', include('guest.urls')),
    path('api/checklist/', include('checklist.urls')),
    path('api/reservation/', include('reservation.urls')),
    path('', include('settings.urls')),
    path('docs/', include_docs_urls(title="Tmmim", permission_classes=[AllowAny]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

