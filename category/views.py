from urllib.parse import quote_plus #python 3
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from posts.models import Post

from django.shortcuts import render
from .models import Category
from .forms import CategoryForm
# Create your views here.

def category_list(request):
	today = timezone.now().date()
	queryset_list = Category.objects.all().order_by("-timestamp")
	query = request.GET.get("q")
	if query: 
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(description__icontains=query)|
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
		"nbar": "category",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "jb_app/category_list.html", context)

def category_create(request):
	if not request.user.is_authenticated and not request.user.is_staff or not request.user.is_superuser:
		raise Http404("Only Staff are allowed to add categories. Please use Contact to send a request to the Admins")
		
	form = CategoryForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False) 
		instance.user = request.user
		instance.save()
		# Without this next line the tags won't be saved.
		form.save_m2m()
		# message success
		messages.success(request, "Category was Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title":"Create Category",  
		"form": form,
	}
	return render(request, "jb_app/category_form.html", context)

def category_detail(request, slug=None):
	category = get_object_or_404(Category, slug=slug)
	posts = category.posts
	queryset_list = posts.filter(draft=False)

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
		"title": category.title,
		"category": category,
		"object_list": queryset,
		"slug":slug,
		"nbar":"category",
		"nbar_detail":"category_detail",
	}
	return render(request, "jb_app/category_details.html", context)

def category_update(request, slug=None):
	if not request.user.is_authenticated and request.user.is_staff or not request.user.is_superuser:
		raise Http404("Only Staff are allowed to update categories. Please use Contact to send a request to the Admins")
	instance = get_object_or_404(Category, slug=slug)
	form = CategoryForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# Without this next line the tags won't be saved.
		form.save_m2m()
		messages.success(request, "Category Updated", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
		
	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "jb_app/category_form.html", context)
    
def category_delete(request, slug=None):
	if not request.user.is_authenticated and request.user.is_staff or not request.user.is_superuser:
		raise Http404("Only Staff are allowed to update categories. Please use Contact to send a request to the Admins")
	instance = get_object_or_404(Category, slug=slug)
	instance.delete()
	messages.success(request, "Category Successfully deleted")
	return redirect("camer-info:category:list")