"""
URL configuration for Student_Help project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Student_Help import settings
from django.conf.urls.static import static

from myapp.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_account/',create_account,name = "create_account" ),
    path('create_account_view/',create_account_view,name = "create_account_view"),
    path('loginn/',login_user,name = "loginn"),
    path('notification/<int:notification_id>/', notification_detail, name='notification_detail'),
    path('login_view/',login_view),
    path('',login_view),
    path('create_post/<type_post>/<token>/',create_post),
    path('create_recommendation/',creation_posts,name="create_post_rec"),
    path('creation_transport/',creation_transport,name="creation_transport"),
    path('creation_logement/',creation_logement,name = "creation_logement"),
    path('creation_stage/',creation_stage,name = "creation_stage"),
    path('all_posts/<token>/', all_posts, name='all_posts'),
    path('my_posts/<token>/', all_posts, name='my_posts'),
    path('like_post/<post_id>/<token>/', like_post, name='like_post'),
    path('getComments/<post_id>/',get_comments),
    path('get_my_posts_view/<token>/',my_posts,name="myposte"),
    path('addComment/<post_id>/<token>/',create_comment),
    path('delete_post/<post_id>/<token>/',delete_post),
    path('userDetails/<token>/',user_details,name="user_profile"),
    path('profileview/<token>/',profile_veiw,name="profile_view"),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)