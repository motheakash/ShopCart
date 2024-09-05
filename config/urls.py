from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path('', include('apps.core.urls')),
    path('api/', include('apps.member_management.urls')),
    path('api/', include('apps.authentications.urls')),
]
