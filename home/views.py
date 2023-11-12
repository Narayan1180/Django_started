from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import FormData
from django.db import models

# Create your views here.


contact_list=[]
def index(request):
    data=FormData.objects.all()
    return render(request,"success.html",{'form_data':data})

def about(request):
    names = ['Alice', 'Bob', 'Charlie']
    return render(request,"about.html",{"names":names})

def services(request):
    #return HttpResponse("this is service page")
    return render(request,"main.html")


def contact(request):
    return render(request,"contact.html")

def Searchcontact(request):
    return render(request,"search_contact.html")

def submit_form(request):
    if request.method == 'POST':
        # Get form data from the request
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Store form data in a dictionary
        form_data = {
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone,
        }
  
        # You can perform additional actions with the form data here
        data = FormData.objects.create(name=name, surname=surname, email=email, phone=phone)
        return redirect("/")
       # contact_list.append(form_data)
        # Return a response (for demonstration purposes)
        #return render(request, 'success.html', {'form_data': contact_list})

    # If the request method is not POST, handle accordingly (e.g., redirect to the form)
    return HttpResponse("Invalid request method.")


def search_contact(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')  # Assuming you have a form with a field named 'search_query'

        # Perform the search based on name, surname, or phone number
        contact = FormData.objects.filter(
            models.Q(name__icontains=search_query) |
            models.Q(surname__icontains=search_query) |
            models.Q(phone__icontains=search_query)
        )

        if contact:
            t=render(request, 'success.html', {'form_data': contact})
            #contact.delete()

            return t
        else:
            return HttpResponse("contact not found")

    
    return render(request, 'search_contact.html')




def delete_contact(request, contact_id):
    contact = get_object_or_404(FormData, id=contact_id)
    print(contact)

    if request.method == 'GET':
        contact.delete()
        return redirect('/')

    return redirect('search_contact')





