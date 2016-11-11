from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
  url(r'^dabba-admin/', admin.site.urls),
  url(r'^', include('supplies.urls')),
  url(r'^', include('supplies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    #   API Endpoints
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/', admin.site.urls),
]
