from django.conf.urls import url, include
from django.contrib import admin

from jb_app.views import (
    home_page,
	contact_page,
	# category_page,
	base_page,
	# login_form_page,
	# register_form_page,
	blog_form_page,
	about_form_page,
	user_profile_view,
	# logout_form_page
	# post_list,
	# post_create,
	# post_detail,
	# post_update,
	# post_delete,
	)
# from accounts.views import (
# 	signup,
# 	activate
# )
app_name = "camer-info"

urlpatterns = [
	url(r'^$', home_page, name='home'),
	url(r'^accounts/profile/', user_profile_view, name="user_profile"), 
	url(r'^contact$', contact_page, name='contact'),
	# url(r'^category$', category_page, name='category'),	
	url(r'^base$', base_page, name='base'),	
	# url(r'^login$', login_form_page, name='login'),
	# url(r'^logout$', logout_form_page, name='logout'),	
    url(r'^category/', include('category.urls', namespace='category')),
	url(r'^blog$', blog_form_page, name='blog'),
	url(r'^about$', about_form_page, name='about'),
	# url(r'^register$', register_form_page, name='register'),
	url(r'^comments/', include("jb_app_comments.urls", namespace='comments')),
	url(r'^posts/', include("jb_app_posts.urls", namespace='posts')),

	# user registration using email
	# url(r'^signup$', signup, name='signup'),
	# url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),

]
