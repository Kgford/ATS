from django.urls import pathfrom django.conf.urls import urlfrom . import viewsfrom django.conf import settingsfrom django.conf.urls.static import staticfrom django.contrib.auth.decorators import login_required, permission_requiredfrom vendors.views import (    VendorView)app_name = "vendors"urlpatterns =[    path('', login_required(VendorView.as_view(template_name="index.html")), name='vendor'),    path("site/<slug:vendor_id>/", views.site, name ="site"),    path("searchsite", views.searchsite, name ="searchsite"),    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    