from django.contrib import adminfrom django.urls import pathfrom django.conf.urls import urlfrom . import viewsfrom django.conf import settingsfrom django.conf.urls.static import staticfrom django.contrib.auth.decorators import login_required, permission_requiredfrom atspublic.views import (    PublicView,    WorkstationView,    RobotView,    FieldView,    SoftwareView,    BlogView,    PostView,    CategoryView,    NewsView,    ContactView,    TestimonialView,    SignupView,)# SET THE NAMESPACE!app_name = 'atspublic'urlpatterns = [    path('admin/', admin.site.urls),    path('', PublicView.as_view(template_name="index.html"), name='public'),    path('workstations/', WorkstationView.as_view(template_name="racks.html"), name='racks'),    path('robot_lab/', RobotView.as_view(template_name="robotLab.html"), name='robot_lab'),    path('field/', FieldView.as_view(template_name="robotLab.html"), name='site'),    path('software/', SoftwareView.as_view(template_name="software.html"), name='software'),    #path('blog/', BlogView.as_view(template_name="blog.html"), name='blog'),    #path('category/', PostView.as_view(template_name="blog.html"), name='news'),    path('newsletter/', NewsView.as_view(template_name="newsletter.html"), name='news'),    path('contact_us/', ContactView.as_view(template_name="contact_us.html"), name='contacts'),    path('testimonials/', TestimonialView.as_view(template_name="contact_us.html"), name='testmonial'),    path('signup/', SignupView.as_view(template_name="signup.html"), name='signup'),    ]