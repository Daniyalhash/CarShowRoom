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

def AdminPanel(request):
    return render(request, 'AdminPanel.html')
from django.contrib.auth.hashers import make_password
def AdminPage(request):
    cars = Car.objects.all()
    return render(request, 'adminPage.html', {'cars': cars})
def AdminLogin(request):
    error_message = None

    if request.method == 'POST':
        # Assign a username and password
        assigned_username = 'admin'
        assigned_password = 'admin'
        
        # Get the username and password from the form
        input_username = request.POST.get('username')
        input_password = request.POST.get('password')

        # Check if the input matches the assigned username and password
        if input_username == assigned_username and input_password == assigned_password:
            # Create a fake user-like dictionary for custom authentication
            user_dict = {
                'username': assigned_username,
                'password': assigned_password,
            }

            # Store the user-like dictionary in the session for authentication
            request.session['user'] = user_dict

            username = user_dict['username']

            return render(request, 'adminPage.html', {'username': username})
        else:
            error_message = "Username or Password is incorrect!!!"

    return render(request, 'AdminPanel.html', {'error_message': error_message})
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

def search(request):
    return HttpResponse('this is searh')
def delete_car(request, car_dashboard_id):
        
    car_dashboard = CarDashboard.objects.get(id=car_dashboard_id)
    car_dashboard.delete()
    
    # Redirect to the desired page after deletion
    return redirect('Dashboard')
    

def add_car(request):
    error_message = None

    if request.method == 'POST':
        # Car details
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        year = request.POST.get('year')
        car_type = request.POST.get('type')

        # Car pricing
        base_price = request.POST.get('base_price')
        premium_package_price = request.POST.get('premium_package_price')
        technology_package_price = request.POST.get('technology_package_price')
        special_offers = request.POST.get('special_offers')

        # Car features
        entry = request.POST.get('entry')
        seats = request.POST.get('seats')
        sunroof = request.POST.get('sunroof')
        system = request.POST.get('system')

        # Car specification
        fuel_type = request.POST.get('fuel_type')
        engine_horsepower = request.POST.get('engine_horsepower')
        engine_torque = request.POST.get('engine_torque')
        transmission = request.POST.get('transmission')
        fuel_efficiency = request.POST.get('fuel_efficiency')
        performance_0_60 = request.POST.get('performance_0_60')
        top_speed = request.POST.get('top_speed')

        # Car color
        color = request.POST.get('color')
        # car image
        color_image_path = request.FILES.get('color_image_path')

        # Garage
        quantity = request.POST.get('quantity')

        # Car video
        video_file = request.FILES.get('video_file')
        description = request.POST.get('description')

        try:
            # Create Car instance and save to database
            car_instance = Car.objects.create(name=name, brand=brand, year=year, type=car_type)

            # Create CarPricing instance and save to database
            car_pricing_instance = CarPricing.objects.create(
                car=car_instance,
                base_price=base_price,
                premium_package_price=premium_package_price,
                technology_package_price=technology_package_price,
                special_offers=special_offers
            )

            # Create CarFeatures instance and save to database
            car_features_instance = CarFeature.objects.create(
                car=car_instance,
                entry=entry,
                seats=seats,
                sunroof=sunroof,
                system=system
            )

            # Create CarSpecification instance and save to database
            car_specification_instance = CarSpecification.objects.create(
                car=car_instance,
                fuel_type=fuel_type,
                engine_horsepower=engine_horsepower,
                engine_torque=engine_torque,
                transmission=transmission,
                fuel_efficiency=fuel_efficiency,
                performance_0_60=performance_0_60,
                top_speed=top_speed
            )
            car_color_name_instance = Color.object.create(color_name=color)
            # Create CarColor instance and save to database
            car_color_instance = CarColor.objects.create(
                color_image_path=color_image_path,
                car=car_instance,
                color=car_color_name_instance,
               
            )

            # Create Garage instance and save to database
            garage_instance = Garage.objects.create(
                car=car_instance,
                quantity=quantity
            )

            # Create CarVideo instance and save to database
            car_video_instance = CarVideo.objects.create(
                car=car_instance,
                video_file=video_file,
                description=description
            )

            # Commit the changes
            car_instance.save()
            car_pricing_instance.save()
            car_features_instance.save()
            car_specification_instance.save()
            car_color_name_instance.save()
            # car_color_instance.save()
            # garage_instance.save()
            # car_video_instance.save()
            return redirect("AdminPage")
            error_message = "saved"
        except Exception as e:
            # Handle exceptions as needed
            error_message = 'An error occurred while saving the car details.'

    return render(request, 'adminPage.html', {'error_message': error_message})

def delete_car_db(request):
    if request.method == 'POST':
        try:
            # Retrieve the car instance
            car_id = request.POST.get('car_id')
            car = get_object_or_404(Car, id=car_id)
            car.delete()

            messages.success(request, 'Car deleted successfully.')
        except Car.DoesNotExist:
            messages.error(request, 'Car not found.')


    return render(request, 'adminPage.html')
def search_update_car(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        try:
            car = get_object_or_404(Car, id=car_id)

            return render(request, 'update.html', {'car': car})
        except Exception as e:
            print(f"Exception: {e}")
            error_message = f"Error: {e}"
            messages.error(request, error_message)
            return render(request, 'adminPage.html', {'error_message': error_message})

    return JsonResponse({'error': 'Invalid request'}, status=400)
def view_cars(request):
    cars = Car.objects.all()
    return render(request, 'adminPage.html', {'cars': cars})    
def update_car(request):
    if request.method == 'POST':
        car_id = request.POST.get('update_car_id')
        car_name = request.POST.get('update_name')

        try:
            car = get_object_or_404(Car, id=car_id)
            car.name = car_name
            # Update other fields if needed
            car.save()

            # Redirect to a success page or another view
            return render(request, 'adminPage.html')

        except Exception as e:
            # Handle exceptions if the car is not found or other errors
            update_error_message = f"Error: {e}"
            return render(request, 'update.html',{'update_error_message': update_error_message})

    # If it's not a POST request, you can handle this part according to your needs
    else:
        return render(request, 'update.html')
    # if request.method == 'POST':
    #     try:
    #         # Retrieve the car instance
    #         car_id = request.POST.get('update_car_id')
    #         car = get_object_or_404(Car, id=car_id)

    #         # Display current values for editing
    #         current_name = car.name
    #         current_brand = car.brand
    #         # Add other fields as needed

    #         # Get new values from the form
    #         new_name = request.POST.get('new_name')
    #         new_brand = request.POST.get('new_brand')
    #         # Get other new values as needed

    #         # Update car details
    #         car.name = new_name
    #         car.brand = new_brand
    #         # Update other fields as needed

    #         car.save()

    #         messages.success(request, 'Car updated successfully.')
    #     except Car.DoesNotExist:
    #         messages.error(request, 'Car not found.')

    # return render(request, 'adminPage.html')

    # # Update car pricing
            # car.base_price = request.POST.get('base_price')
            # car.premium_package_price = request.POST.get('premium_package_price')
            # car.technology_package_price = request.POST.get('technology_package_price')
            # car.special_offers = request.POST.get('special_offers')

            # # Update car features
            # car.entry = request.POST.get('entry')
            # car.seats = request.POST.get('seats')
            # car.sunroof = request.POST.get('sunroof')
            # car.system = request.POST.get('system')

            # # Update car specifications
            # car.fuel_type = request.POST.get('fuel_type')
            # car.engine_horsepower = request.POST.get('engine_horsepower')
            # car.engine_torque = request.POST.get('engine_torque')
            # car.transmission = request.POST.get('transmission')
            # car.fuel_efficiency = request.POST.get('fuel_efficiency')
            # car.performance_0_60 = request.POST.get('performance_0_60')
            # car.top_speed = request.POST.get('top_speed')

            # # Update car color
            # car.color = request.POST.get('color')
            # car.color_image_path = request.POST.get('color_image_path')

            # # Update garage
            # car.quantity = request.POST.get('quantity')

            # # Update car video and description
            # car.video_file = request.POST.get('video_file')
            # car.description = request.POST.get('description')

            # Save the updated car instance