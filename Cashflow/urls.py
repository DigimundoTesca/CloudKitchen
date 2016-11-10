from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
  url(r'^tesca-admin/', admin.site.urls),
  url(r'^', include('supplies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
