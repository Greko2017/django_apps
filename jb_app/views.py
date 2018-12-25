from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )

try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from posts.models import Post
from accounts.models import SignUp
from accounts.forms import UserLoginForm, UserRegisterForm, ContactForm, SignUpForm

def home_page(request):

	context = {
		"title": "Camer-Info+",
		'nbar': 'home'
	}
	return render(request, "jb_app/index.html", context)

def contact_page(request):
	title = 'Contact Us'
	title_align_center = True
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
		# 	#print form.cleaned_data.get(key)
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = '[Camer Info+] Contact Form message'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'gregory.goufan@hotmail.fr']
		contact_message = "%s: %s via %s"%( 
				form_full_name, 
				form_message, 
				form_email)
		# some_html_message = """
		# <h1>hello</h1>
		# """
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				html_message=some_html_message,
				fail_silently=False)

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center,
		'nbar': 'contact',
	}
	return render(request, "jb_app/contact.html", context)

def blog_form_page(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
		"nbar":'blog',
	}
	return render(request, "jb_app/category.html", context)

def base_page(request):
	title = 'Here is a base'
	context = {
		"title": title,
	}
	return render(request, "jb_app/base.html", context)

def login_form_page(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("camer-info:home")
	return render(request, "jb_app/login_form.html", {"form":form, "title": title})

def register_form_page(request):
	next = request.GET.get('next')
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect('/')
	return render(request, 'jb_app/register_form.html', {"form":form, "title":title, 'nbar':'register'})

# def blog_form_page(request):
# 	title = 'Here is a blog_form'
# 	context = {
# 		"title": title,
# 	}
# 	return render(request, "jb_app/post_details.html", context)

def about_form_page(request):
	title = 'Here is a about_form'
	context = {
		"title": title,
		'nbar': 'about',
	}
	return render(request, "jb_app/regular.html", context)

def logout_form_page(request):
    logout(request)
    return redirect("camer-info:home")

# def bad_request(request, exception):
#     context = RequestContext(request)
#     err_code = 400
#     response = render_to_response('error/400.html', {"code":err_code}, context)
#     response.status_code = 400
#     return response

# def permission_denied(request, exception):
#     context = RequestContext(request)
#     err_code = 403
#     response = render_to_response('error/403.html', {"code":err_code}, context)
#     response.status_code = 403
#     return response

# def page_not_found(request, exception):
#     context = RequestContext(request)
#     err_code = 404
#     response = render_to_response('error/404.html', {"code":err_code}, context)
#     response.status_code = 404
#     return response

# def server_error(request, exception):
#     context = RequestContext(request)
#     err_code = 500
#     response = render_to_response('error/500.html', {"code":err_code}, context)
#     response.status_code = 500
#     return response

# def csrf_403(request, exception):
# 	context = RequestContext(request)
# 	err_code = '403_csrf'
# 	response = render_to_response('403_csrf.html', {"code":err_code}, context)
# 	response.status_code = 403
# 	return response
