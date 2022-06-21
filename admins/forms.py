
from pyexpat import model
from django.forms import ModelForm
from products.models import Product,Review,Category


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            "category",
            "name",
            "image",
            "image1",
            "image2",
            "description",
            "price",
            "status",
            "stock",
        )
    def __init__(self,*args,**kwargs):
        super(AddProductForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"