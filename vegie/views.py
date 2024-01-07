from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.db import *
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.

@login_required(login_url="/login") #login in required without this you can,t access receipes
def recipes(request):

    if request.method=="POST":
        
        data=request.POST
        recipe_name =data.get('receipe_name')
        recipe_description=data.get('receipe_description')
        recipe_image = request.FILES.get('receipe_image')

        Recipe.objects.create(recipe_name=recipe_name,recipe_description=recipe_description,recipe_image=recipe_image)
#print(recipe_name)
        #print(recipe_description)
       # print(recipe_image)

    data=Recipe.objects.all()
    print(data)
    return render(request,"receipes.html",{'items':data})


def delete_recipe(request, recipe_id):

    del_recipe = get_object_or_404(Recipe, id=recipe_id)
    print(del_recipe,request.method)
    if request.method == 'GET':
        del_recipe.delete()
        return redirect('receipes')
    

    return redirect("receipes/")


def update_recipe(request, recipe_id):

    update_recipe = Recipe.objects.get(id=recipe_id)
    if request.method=="POST":
        data=request.POST
        recipe_name =data.get('receipe_name')
        recipe_description=data.get('receipe_description')
        recipe_image = request.FILES.get('receipe_image')

        update_recipe.recipe_name=recipe_name
        update_recipe.recipe_description=recipe_description

        if recipe_image:
            update_recipe.recipe_image=recipe_image

        update_recipe.save()
        
        return redirect("receipes")



    return render(request,"update_recipe.html",{"update_recipe":update_recipe})


def login_page(request):

    if request.method=="POST":

        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():

            messages.error(request,'Invalid User')

            return redirect('/login')
        
        user = authenticate(username=username,password=password)
        print(user)
        if user is None:
            messages.error(request,'Invalid Credentials')
            return redirect('/login')
        
        else:
            login(request,user) #done by django

            return redirect('/receipes')
        



    return render(request,"login.html")

def register_page(request):

    if request.method=="POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user =User.objects.filter(username=username)

        if user.exists():
           
            return redirect("/register")
        
        user=User.objects.create(first_name=first_name,last_name=last_name,username=username)

        user.set_password(password) # we are setting pasword after creating user for encryption purpose 

        user.save()
        messages.info(request,"Accounts Created successfully")
        return redirect("/register")
       
        
    

    return render(request,"register.html")


# views.py


def recipe_search(request):
    query = request.GET.get('query', '')
    print(f"query: {query}")
   
    if query:
        results = Recipe.objects.filter(recipe_name__icontains=query )|  Recipe.objects.filter(recipe_description__icontains=query )

    print(f"Results: {results}")
    return render(request, 'recipe_search.html', { 'query':query,'results': results})


def logout_page(request):
    logout(request)

    return redirect("/login")




