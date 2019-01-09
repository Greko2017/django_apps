from django.conf.urls import url, include
from django.contrib import admin

from category.views import ( 
    category_list,
    category_create,
    category_detail,
    category_update,
    category_delete,
	)
app_name = "category"
 
urlpatterns = [
	url(r'^$', category_list, name='list'),
    url(r'^create/$', category_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/$', category_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', category_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', category_delete, name="delete"),

]