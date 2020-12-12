from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from atspublic import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='public'),
    path('staff/', include("users.urls")),
    path('', include("atspublic.urls")),
    path('inventory/', include("inventory.urls"),name='inven'),
    path('locations/', include("locations.urls")),
    path('equipment/', include("equipment.urls")),
    path('accounting/', include("accounting.urls")),
    path('vendors/', include("vendors.urls")),
    path('clients/', include("clients.urls"),name='client'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
