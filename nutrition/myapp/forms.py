from django.forms import ModelForm
#from models import Order
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class createuserForm(UserCreationForm):
    
    email =forms.EmailField(required=True,max_length=40)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        # def save(self, commit=True):
        #            user= super(createuserForm, self).save(commit=False)
        #            user.email = self.cleaned_data['email']
        #            if commit:
        #               user.save()

        #            return user
class ContactForm(forms.Form):
    #subject = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)
    email_address = forms.EmailField(max_length = 150)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)   
		   
		   
			