from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('users.urls')),
    url(r'^', include('branchoffices.urls')),
    url(r'^', include('products.urls')),
    url(r'^', include('sales.urls')),
    url(r'^', include('orders.urls')),
]

admin.site.site_header = 'Dabbanet'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
