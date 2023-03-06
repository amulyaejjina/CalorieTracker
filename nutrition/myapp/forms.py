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
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

        # def save(self, commit=True):
        #            user= super(createuserForm, self).save(commit=False)
        #            user.email = self.cleaned_data['email']
        #            if commit:
        #               user.save()

        #            return user
		    
		   
		   
		   
			
