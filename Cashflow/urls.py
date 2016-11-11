from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.authtoken import views

urlpatterns = [
  url(r'^dabba-admin/', admin.site.urls),
  url(r'^', include('supplies.urls')),
  url(r'^', include('supplies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    #   API Endpoints
    url(r'^api/v1/', include('restapp.urls', namespace='restapp')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
