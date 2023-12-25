# myapp/views.py
from django.shortcuts import get_object_or_404, render, redirect
import uuid
import re
from django.http import JsonResponse
from django.http import HttpResponse
import sqlite3
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import sqlite3,os,datetime,random,string
from pathlib import Path
from .models import Color, Car, CarPricing, CarSpecification, CarColor, Garage,CarFeature 
from uuid import UUID
from django.views.decorators.csrf import csrf_protect
from .models import Payment
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
BASE_DIR = Path(__file__).resolve().parent.parent
from django.conf import settings

from django.db import IntegrityError
from django.contrib import messages

from django.conf import settings
# With this line
from django.utils.encoding import force_bytes
# Create your views here.
@login_required(login_url='Login')
def myview(request):
    cars = Car.objects.all()
    return render(request, 'index.html', {'cars': cars})


def Signup(request):
    error_message = None

    if request.method == 'POST':
        unameF = request.POST.get('usernameFirst')
        unameL = request.POST.get('usernameLast')
        uname = f"{unameF}{unameL}"  # Combine first and last name
        email = request.POST.get('Email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if all fields are filled
        if not unameF or not unameL or not email or not pass1 or not pass2:
            error_message = 'Please fill in all fields.'

        # Check if passwords match
        elif pass1 != pass2:
            error_message = 'Passwords do not match.'

        # Check password length
        elif len(pass1) < 8:
            error_message = 'Password must be at least 8 characters long.'

        else:
            try:
                # Check if the email already exists in the database
                if User.objects.filter(email=email).exists():
                    error_message = 'Email is already taken. Please use a different one.'
                else:
                    # Try to create the user
                    my_user = User.objects.create_user(uname, email, pass1)
                    my_user.save()
                    
                    # Display a success message
                    messages.success(request, 'Account created successfully. You can now log in.')
                    # Send confirmation email
                   # Send welcome email
                 

                    # Redirect to the login page
                    return redirect('Login')

            except IntegrityError as e:
                # Check if the IntegrityError is due to a unique constraint violation
                if 'UNIQUE constraint failed' in str(e):
                    error_message = 'Username is already taken. Please choose a different one.'
                else:
                    # Handle other IntegrityError cases or re-raise the exception
                    raise e
    return render(request, 'Signup.html', {'error_message': error_message})
# def send_email(request):
#     return redirect("Login")
# def send_email_to_client(request):
#     subject = 'Welcome to Wheels!'
#     message = 'Thank you for joining Wheels! We are excited to have you as a member.'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = ['syeddaniyalhashmi890@gmail.com']
#     print('email gone')
#     send_mail(subject, message, from_email, recipient_list)


def Login(request):
    error_message = None

    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            username = username

            # You can also store the user_name in the session if needed
           
            return render(request, 'index.html', {'username': username})
        else:
            error_message = "Username or Password is incorrect!!!"

    return render (request,'Login.html', {'error_message': error_message})

def Logout(request):
    logout(request)
    return redirect('Login')
def Contact(request):

    return render(request, 'contact.html')
def About(request):

    return render(request, 'about.html')
def like(request):
    # Fetch all liked cars
    liked_cars = Like.objects.filter(user=request.user)
    return render(request, 'like.html', {'liked_cars': liked_cars})
def message_us(request):
    if request.method == 'POST':
        full_name = request.POST.get('Full')
        message_text = request.POST.get('message')

        # Create and save the Message instance
        Message.objects.create(full_name=full_name, message=message_text)

        return redirect('Contact')  # Redirect to a success page or any other page

    return render(request, 'contact.html')
def add_to_whislist(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Check if the user has already liked the car
    existing_like = Like.objects.filter(car=car, user=request.user)
    if existing_like.exists():
        # User has already liked the car, you may want to handle this case
        message = "You have already added this car to your wishlist."
    else:
        # User hasn't liked the car, create a new Like instance
        Like.objects.create(car=car, user=request.user)
        message = "Car added to your wishlist successfully."

    return redirect('Shop')
def remove_from_wishlist(request, id):
    car = get_object_or_404(Car, id=id)

    # Check if the user has already added the car to the wishlist
    existing_like = Like.objects.filter(car=car, user=request.user)

    if existing_like.exists():
        # User has added the car to the wishlist, delete the Like instance
        existing_like.delete()
        message = "Car removed from your wishlist successfully."
    else:
        # User hasn't added the car to the wishlist, handle this case
        message = "You haven't added this car to your wishlist."

    # Redirect back to the 'like' page
    return redirect('like')
def Shop(request):
    cars = Car.objects.all()
    return render(request, 'shop.html', {'cars': cars})

def Dashboard(request):
    # Assuming you have user information in the request
    user_id = request.user.id  # Adjust this based on your user setup

    # Query CarDashboard entries for the current user
    user_cars = CarDashboard.objects.filter(user_id=user_id)

    # Create a list to store car details (including color image)
    user_cars_details = []

    for user_car in user_cars:
        car = user_car.car
        colors = CarColor.objects.filter(car=car)  # Fetch color details for the car

        # Choose one color (you might want to implement your logic here)
        color = colors.first()  # Change this line based on your logic

        # Append car details with color image to the list
        user_cars_details.append({
            'car_dashboard_id': user_car.id,
            'car_name': car.name,
            'car_year': car.year,
            'car_model': car.type,
            'color_image_path': color.color_image_path.url,  # Assuming color_image_path is an ImageField
        })

    # Pass the user's cars with color details to the template
    context = {'user_cars_details': user_cars_details}

    return render(request, 'Dashboard.html', context)
def Product(request, id):
    # Fetch the specific car based on the provided id
    car = get_object_or_404(Car, id=id)

    # Fetch related objects
    pricing = get_object_or_404(CarPricing, car=car)
    specification = get_object_or_404(CarSpecification, car=car)

    # Fetch colors associated with the car
    colors = CarColor.objects.filter(car=car)

    # Create a dictionary to store color_id as keys and corresponding images as values
    color_images = {}

    # Populate the color_images dictionary
    # Populate the color_images dictionary
    for color in colors:
        color_id = color.color.id
        color_name = color.color.color_name  # Access the color_name through the foreign key
        color_images[color_id] = {'color_name': color_name, 'image_path': color.color_image_path}

        
    features = get_object_or_404(CarFeature, car=car)
    total_price = pricing.base_price + pricing.technology_package_price + pricing.premium_package_price
    # Check if the car is in the garage and has available quantity
     # Fetch videos associated with the car
    car_videos = CarVideo.objects.filter(car=car)
    return render(request, 'product.html', {
        'car': car,
        'pricing': pricing,
        'specification': specification,
        'colors': colors,
        'features': features,
        'total_price': total_price,
        'color_images': color_images,
        'car_videos': car_videos,
    })
@csrf_protect
def Payment(request, user_id, car_id):
    # Fetch the specific car based on the provided id
    car = get_object_or_404(Car, id=car_id)

    # Your existing logic for colors (make sure it's fetching the correct data)
    user_id = user_id

    # Initialize color_id to None
    color_id = None

    if request.method == 'POST':
        # Assuming you have a form with 'selectedColorId' field
        selected_color_name = request.POST.get('selectedColorId')
        selected_color_id = request.POST.get('selectedColoredId')

        # Add your logic for processing the form data here
        color_name = selected_color_name
        color_id = selected_color_id
        print(color_name)
         # You need to define 'payment_success' URL in your urls.py
        # return HttpResponse('heelo',selected_color_id)
    return render(request, 'Payment.html', {
        'car': car,
        'color_name': color_name,  # Pass the color_id to the template
        'user_id': user_id,
        'color_id': color_id,
    })
from django.shortcuts import get_object_or_404
import uuid
from django.db import models
from .models import Car
def save_data(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        car_id = request.POST.get('car')
        color_id = request.POST.get('color_id')
        car = get_object_or_404(Car, pk=car_id)

         # Check if the car is in the garage and has available quantity
        garage_entry = get_object_or_404(Garage, car=car)
        if garage_entry.quantity <= 0:
            error_message = "Sorry, this product is out of stock. Please choose another product."
            return render(request, 'celebration.html', {'error_message': error_message})
        name = request.POST.get('name')
        card_number = request.POST.get('cardNumber')
        exp_1 = request.POST.get('exp-1')
        exp_2 = request.POST.get('exp-2')
        phone = request.POST.get('phone')
        expiration_date = f"{exp_1}/{exp_2}"
        cvc = request.POST.get('cvc')
        # Retrieve the Car object
        color_id= int(color_id)
        color = get_object_or_404(Color, pk=color_id)

        car = get_object_or_404(Car, pk=car_id)
        # Create a new CarDashboard entry with user_id, car, and color
        car_dashboard_entry = CarDashboard(user_id=user_id, car=car,color=color)
        car_dashboard_entry.save()
        payment = system(name=name, card_number=card_number, expiration_date=expiration_date, security_code=cvc, car_id=car_id)
       
        payment.save()
       # Update the garage quantity
        garage_entry.quantity -= 1
        garage_entry.save()

        return redirect('Celebration', car_id=car_id, color_id=color_id,user_id=user_id)

    return HttpResponse("Invalid request method")


    # Continue with the rest of your view logic...

from django.http import Http404
from django.shortcuts import render
from .models import Car, CarColor, CarDashboard

def Celebration(request, car_id, color_id, user_id):
    try:
        # Fetch the specific car and color based on the provided ids for the user
        car = get_object_or_404(Car, id=car_id)
        color = get_object_or_404(Color, id=color_id)

        # Fetch the CarColor associated with the chosen color
        car_color = CarColor.objects.filter(car=car, color=color).first()
        if not car_color:
            raise Http404("CarColor not found")

        color_image_path = car_color.color_image_path.url

        user_name = request.user.username  # Adjust this based on your user model
        user_id = user_id

        return render(request, 'celebration.html', {
            'car': car,
            'color': color,
            'user_name': user_name,
            'user_id': user_id,
            'color_image_path': color_image_path,
        })
    except Car.DoesNotExist:
        raise Http404("Car not found")
    except Color.DoesNotExist:
        raise Http404("Color not found")
    except CarColor.DoesNotExist:
        raise Http404("CarColor not found")
# def search_car(request):

#     if request.method == 'POST':
#         car_name = request.POST.get('car_name')
#         car = get_object_or_404(Car, name=car_name)
#         car_colors = CarColor.objects.filter(car=car)

#         # Return JSON response
#         car_details = {
#             'name': car.name,
#             'brand': car.brand,
#             'year': car.year,
#             'type': car.type,
#             'colors': [{'color_name': color.color.color_name, 'image_path': color.color_image_path.url} for color in car_colors]
#         }

#         return JsonResponse({'success': True, 'car_details': car_details})

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})
def search(request):
    return HttpResponse('this is searh')
def delete_car(request, car_dashboard_id):
        
    car_dashboard = CarDashboard.objects.get(id=car_dashboard_id)
    car_dashboard.delete()
    
    # Redirect to the desired page after deletion
    return redirect('Dashboard')
    

