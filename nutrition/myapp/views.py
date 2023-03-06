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

def home(request):
    connect = connection.cursor()
    if request.method =="GET":
        with connection.cursor() as cursor:
            food_searched = request.GET.get('food_searched')
            food_searched = 'Oatmeal'
            # food_consumed = request.GET['food_consumed']
            print("-----------")
            print(food_searched)
            query = "SELECT name,carbs,protein,fats,calories FROM myapp_food WHERE name="+"'"+food_searched+"'"
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        return render(request, 'myapp/home.html', {'columns': columns, 'data': data})
 
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
            messages.success(request,f'account created')
            return redirect('home')
        messages.error(request,f'account created')
    form = createuserForm()
        
    context ={'form':form}    
    return render(request, 'myapp/register.html',context)
    return render (request=request, template_name="myapp/register.html", context={"register_form":form})

def loginpage(request):
    #context ={}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
         form = AuthenticationForm(request, data=request.POST)
         if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Hello <b>{user.username}</b>!You are now logged in as {username}.")

            else:
                messages.error(request,"Invalid username or password.")
         else:
             messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    #context ={'form':form} 
    return render(request=request, template_name="myapp/login.html", context={"login_form":form})
    #return render(request, 'myapp/login.html',context)
    
def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
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
 
def delete_consume(request,id):
    consumed_food = Consume.objects.get(id=id)
    if request.method =='POST':
        consumed_food.delete()
        return redirect('/')
    return render(request,'myapp/delete.html')

def index(request):
    return render(request,'myapp/signup.html')

def contact(request):
    return render(request,'myapp/contact.html')

def test(request):
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        
        # get curren user object
        user = request.user

        consume = Consume(user=1,food_consumed=consume)
        consume.save()
        foods = Food.objects.all()
 
    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=1)
 
    # return render(request,'myapp/index.html',{'foods':foods,'consumed_food' : consumed_food})
 
    return render(request,"myapp/ind.html",{'foods':foods,'consumed_food' : consumed_food})

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
 