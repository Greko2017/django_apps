from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown
from comments.models import Comment
from taggit.managers import TaggableManager 
from django.core.exceptions import ObjectDoesNotExist

from posts.utils import get_read_time 

# Create your models here.
  
# app_label = "category"

class CategoryManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(self, **kwargs) 
        except ObjectDoesNotExist:
            return None

    def get_all_category(self, *args, **kwargs):
        return super(CategoryManager, self).order_by("title")

    def get_first_three_categories(self, *args, **kwargs):
        return super(CategoryManager, self).order_by("-timestamp")[:3]

    def get_first_three_existing_categories(self, *args, **kwargs):
        categories = Category.objects.order_by("-timestamp")
        i=0        
        f=0
        existing_categories=[]  
        while 1==1:
            for category in categories:
                if (Category.objects.get(slug=category.slug)).posts.exists():
                    existing_categories.append(Category.objects.filter(pk=category.pk).first())
                    i=i+1
                    # print("true", i)
                    # print((Category.objects.get(slug=category.slug)))
                    # print((Category.objects.get(slug=category.slug)).posts)
                    if i==2:
                        break
                else:
                    # print("false")
                    f=f+1
            if i==3 or f==10:
                # print("break")
                break
        # print(existing_categories)
        return existing_categories

def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.id, instance.id, extension)

class Category(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    slug = models.SlugField(unique=True) 
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field =models.IntegerField(default=0)
    width_field = models.IntegerField(default=0) 
    tags = TaggableManager()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = CategoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("camer-info:category:detail", kwargs={"slug": self.slug})
    class Meta:
        ordering = ["-timestamp", "-updated"]
    


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Category.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_category_receiver, sender=Category)