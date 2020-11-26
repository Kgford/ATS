from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from inventory.views import (
    PublicView,
    WorkstationView,
    RobotView,
    FieldView,
    SoftwareView,
    BlogView,
    PostView,
    CategoryView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('public', PublicView.as_view(template_name="index.html"), name='publid'),
    path('workstations', WorkstationView.as_view(template_name="racks.html"), name='racks'),
    path('robot_lab', RobotView.as_view(template_name="robotLab.html"), name='lab'),
    path('field', FieldView.as_view(template_name="robotLab.html"), name='site'),
    path('software', SoftwareView.as_view(template_name="software.html"), name='web'),
    path('blog', BlogView.as_view(template_name="blog.html"), name='blog'),
    path('category', PostView.as_view(template_name="blog.html"), name='view_blog_post'),
    path('post', CategoryView.as_view(template_name="blog.html"), name='view_blog_post'),
]
