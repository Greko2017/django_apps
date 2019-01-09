from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post, Category


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "content",
            "image",
            "draft",
            "tags",
            "publish",
        ]