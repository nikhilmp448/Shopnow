from types import ClassMethodDescriptorType
from django import forms
from django.forms import fields  
from . models import Account, Address



class RegistrationForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields=['first_name','last_name','email','mobile','gender','password']
        

    def __init__(self,*args,**kwargs):
        super(RegistrationForm ,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data    =super(RegistrationForm,self).clean()
        password        =cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
            
class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['full_name','address','city','pin_code','state','country','mobile','landmark']
        

    def __init__(self,*args,**kwargs):
        super(AddressForm ,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'