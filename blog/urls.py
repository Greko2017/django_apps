import allauth
from django.conf import settings
from django.conf.urls import include, url  
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views 
import re 
# from accounts.views import (login_view, register_view, logout_view, user_profile_view)
 
urlpatterns = [  

    # url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^accounts/profile/', user_profile_view, name="user_profile"),
    url(r'^comments/', include("comments.urls", namespace='comments')), 
    url(r'^users/', include('jb_users.urls', namespace='users')),
    # url(r'^register/', register_view, name='register'),
    # url(r'^login/', login_view, name='login'),
    # url(r'^logout/', logout_view, name='logout'),
    url(r'^', include("jb_app.urls", namespace='camer-info')),    
    url(r'old-home^', include("posts.urls", namespace='posts')),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)