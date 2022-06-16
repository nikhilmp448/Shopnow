from django import forms
from django.db import models
from django.db.models import fields
from .models import Category


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug")

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"