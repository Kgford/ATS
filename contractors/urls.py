from django.urls import pathfrom datetime import datetimefrom django.conf.urls import url,includefrom . import viewsfrom django.conf import settingsfrom django.conf.urls.static import staticfrom django.contrib.auth import views as auth_viewsfrom django.contrib.auth.decorators import login_required, permission_requiredfrom contractors.views import (    ContractorView)app_name = "contractors"urlpatterns =[     path('login/',         auth_views.LoginView.as_view         (             template_name='users/login.html',             extra_context=             {                 'title': 'Log in',                 'year' : datetime.now().year,             }         ),         name='user_login'),    path('', login_required(ContractorView.as_view(template_name="index.html")), name='contractor'),    path("site/<slug:contractor_id>/", login_required(views.site), name ="site"),    path("searchsite", login_required(views.searchsite), name ="searchsite"),    path('staff/', include("users.urls")),    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    