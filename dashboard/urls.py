from django.urls import pathfrom django.conf.urls import url,includefrom django.contrib.auth import views as auth_viewsfrom django.conf import settingsfrom django.conf.urls import url,includefrom django.conf.urls.static import staticfrom django.conf import settingsfrom . import viewsfrom django.contrib.auth.decorators import login_required, permission_requiredfrom dashboard.views import (    DashboardView,    UserLogin)app_name = "dashboard"urlpatterns =[    path('', login_required(DashboardView.as_view(template_name="index.html")), name='dashboard'),    path('login', login_required(UserLogin.as_view(template_name="user_login.html")), name='login'),    path('staff/', include("users.urls")),    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        