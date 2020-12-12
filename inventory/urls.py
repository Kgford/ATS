from django.urls import pathfrom django.conf.urls import url,includefrom . import viewsfrom django.conf import settingsfrom django.conf.urls.static import staticfrom django.contrib.auth.decorators import login_required, permission_requiredfrom inventory.views import (    InventoryView,    SearchView)app_name = "inventory"urlpatterns =[	path('', login_required(InventoryView.as_view(template_name="index.html")), name='inven'),	url(r'^$', SearchView.as_view(), name='search'),	path("update_inv", views.update_inv, name ="update_inv"),	path("save_event", views.save_event, name ="save_event"),	path("items", views.items, name ="items"),	path("item", views.item, name ="item"),	path("report", views.report, name ="report"),	path("inv_report", views.inv_report, name ="inv_report"),	path("upload_file", views.upload_file, name ="upload_file"),    path('staff/', include("users.urls")),    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    