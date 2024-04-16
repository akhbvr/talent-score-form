from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk'))
    ]
