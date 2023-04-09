from django.shortcuts import render, redirect
from .models import Food,Consume
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import createuserForm
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Food,Consume
from django.db import connection
from django.contrib.auth.models import User
from django import forms
from .forms import ContactForm,Loginform
from django.core.mail import send_mail, BadHeaderError

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# import factory
# from factory.django import DjangoModelFactory

# class UserFactory(DjangoModelFactory):

#     username = factory.Sequence('testuser{}'.format)
#     email = factory.Sequence('testuser{}@company.com'.format)

#     class Meta:
#         model = User

def home(request):
    connect = connection.cursor()
    if request.user.is_authenticated:
        return redirect('/test/')
    elif request.method =="GET":
        data=''
        columns=''
        with connection.cursor() as cursor:
            food_searched = request.GET.get('food_searched')
            
            if food_searched is None:
                food_searched = ''
            else:
                food_searched = food_searched.lower()
            # food_searched = 'Oatmeal'
            # food_consumed = request.GET['food_consumed']

                # query = "SELECT name,carbs,protein,fats,calories FROM myapp_food WHERE LOWER(name) LIKE '%{}'".format(food_searched.lower())
                #query = "SELECT name, carbs, protein, fats, calories FROM myapp_food WHERE LOWER(name) LIKE '"+food_searched.lower()+"%'"
                #query = "SELECT name,carbs,protein,fats,calories FROM myapp_food WHERE LOWER(name) LIKE '"+food_searched.lower()+"%'"

                query = "SELECT name,carbs,protein,fats,calories FROM myapp_food WHERE LOWER(name)="+"'"+food_searched+"'"
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
        return render(request, 'myapp/home.html', {'columns': columns, 'data': data})
 
    elif request.method =="POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        # get curren user object
        user = request.user

        consume = Consume(user=user,food_consumed=consume)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
        #  consumed_food = Consume.objects.filter(user=request.user)
    #{'foods':foods,'consumed_food' : consumed_food}
    return render(request, 'myapp/home.html')#,{'foods':foods,'consumed_food' : consumed_food,'columns': columns, 'data': data})

def register(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/")
    form = createuserForm()
    if request.method=='POST':
        form =createuserForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, user)
            messages.success(request,f'"User Accout created"')
            return redirect('/login')
        for error in list(form.errors.values()):
             messages.error(request, error)
    form = createuserForm()
        
    context ={'form':form}    
    return render(request, 'myapp/register.html',context)
    return render (request=request, template_name="myapp/register.html", context={"register_form":form})

def loginpage(request):
    context ={}
    if request.user.is_authenticated:
        return redirect('/test/')
    elif request.method == "POST":
         form = Loginform(request, data=request.POST)
         if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if (len(username) == 0) or (len(password) == 0):
                return redirect('/login/')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # request.session['user'] = user
                return redirect('/test/')
            else:
                for error in list(form.errors.values()):
                     messages.error(request, error)
         else:
            print("Coming in else")
            for error in list(form.errors.values()):
                     messages.error(request, error)
            return redirect('/login/')
    form = Loginform()
    context ={'form':form} 
    return render(request=request, template_name="myapp/login.html", context={"login_form":form})
    #return render(request, 'myapp/login.html',context)
    
def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return render(request,"myapp/home.html")

# Create your views here.
def index(request):
 
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        
        # get curren user object
        user = request.user

        consume = Consume(user=user,food_consumed=consume)
        consume.save()
        foods = Food.objects.all()
 
 
    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
 
    return render(request,'myapp/index.html',{'foods':foods,'consumed_food' : consumed_food})

def check_bmi(request):
    return render(request,'myapp/bmi.html')
def MealPlan(request):
    return render(request, 'myapp/mealplan.html' )

# def mealplan(request):
#     return render(request,'myapp/meal.html')

def delete_consume(request,id):
    consumed_food = Consume.objects.get(id=id)
    user = request.user
    if request.method =='POST':
        consumed_food.delete()
        return redirect('/test/')
    return render(request,'myapp/delete2.html',{'username' : user.username})

def index(request):
    return render(request,'myapp/signup.html')

# def contact(request):
#     return render(request,'myapp/contact.html')

def test(request):
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        if not request.user.is_authenticated:
            request.user.id = 1
        # get current user object
        user = request.user
        
        consume = Consume(user=user,food_consumed=consume)
        consume.save()
        foods = Food.objects.all()
 
    else:
        foods = Food.objects.all()
        # user = request.user
    user = request.user
    consumed_food = Consume.objects.filter(user=request.user.id)
 
    # return render(request,'myapp/index.html',{'foods':foods,'consumed_food' : consumed_food})
 
    return render(request,"myapp/ind_backup.html",{'foods':foods,'consumed_food' : consumed_food,'username' : user.username})

def search(request):
    pass
    # connect = connection.cursor()
    # if request.method =="GET":
    #     with connection.cursor() as cursor:
    #         food_consumed = request.GET['food_consumed']
    #         query = "SELECT name,carbs,protein,fats,calories FROM myapp_food WHERE name="+"'"+food_consumed+"'"
    #         cursor.execute(query)
    #         columns = [col[0] for col in cursor.description]
    #         data = cursor.fetchall()
    #     return render(request, 'myapp/index.html', {'columns': columns, 'data': data})
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "myapp/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'no-reply@Carlorietracker.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with  password reset instructions has been sent to your inbox.')
					return redirect ("/password_reset")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="myapp/password_reset.html", context={"password_reset_form":password_reset_form})

def contact(request):
     if request.method=='POST':
          form =ContactForm(request.POST)

          if form.is_valid():
               subject = "Website Inquiry"
               body = {
			'first_name': form.cleaned_data['first_name'], 
			'last_name': form.cleaned_data['last_name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
               message = "\n".join(body.values())
               try:
                send_mail(subject,message,'admin@example.com', ['admin@example.com'],fail_silently=False),
                messages.success(request, 'Thank you,Message submited successfully!')
               except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                    for error in list(form.errors.values()):
                         messages.error(request, error)
               return redirect('/contact')
     form =ContactForm()
     return render(request, "myapp/contact.html", {'form':form})

    

