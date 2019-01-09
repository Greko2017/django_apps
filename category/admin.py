from django.contrib import admin

# Register your models here.
from .models import Category


class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ["title", "description"]
	list_editable =["description"]
	list_display_links = []
	list_filter = ["title"]
	search_fields = ["title", "description"]
	class Meta:
		model = Category

admin.site.register(Category, CategoryModelAdmin)