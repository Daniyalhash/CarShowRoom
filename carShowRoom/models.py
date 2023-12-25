from django.db import models
import uuid

from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User

class Color(models.Model):
    color_name = models.CharField(max_length=255)

    def __str__(self):
        return self.color_name

class Car(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='Unknown')
    year = models.IntegerField(default=datetime.now().year)
    type = models.CharField(max_length=255,default='Sedan')

    def __str__(self):
        return self.name

class CarPricing(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    premium_package_price = models.DecimalField(max_digits=10, decimal_places=2)
    technology_package_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_offers = models.TextField()

    def __str__(self):
        return f"Pricing for {self.car.name}"



class CarSpecification(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=255)
    engine_horsepower = models.IntegerField()
    engine_torque = models.IntegerField()
    transmission = models.CharField(max_length=255)
    fuel_efficiency = models.DecimalField(max_digits=5, decimal_places=2)
    performance_0_60 = models.DecimalField(max_digits=5, decimal_places=2)
    top_speed = models.IntegerField()

    def __str__(self):
        return f"Specification for {self.car.name}"

class CarColor(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    color_image_path = models.ImageField(upload_to='color_images/')

    def __str__(self):
        return f"{self.car.name} - {self.color.color_name}"



class Garage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {self.car.name}(s) in the garage"

class CarFeature(models.Model):
    car = models.OneToOneField('Car', on_delete=models.CASCADE)
    entry = models.CharField(max_length=255)
    seats = models.CharField(max_length=255)
    sunroof = models.CharField(max_length=255)
    system = models.CharField(max_length=255)

    def __str__(self):
        return f"Features for {self.car.name}"
class Like(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.car.name}"

# models.py
from datetime import date  # Import the date module



class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    security_code = models.CharField(max_length=4)
    def __str__(self):
        return f"Payment for {self.car.name} by {self.name}"
class system(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    security_code = models.CharField(max_length=4)
    payment_date = models.DateField(default=date.today)


    def __str__(self):
        return f"Payment for {self.car.name} by {self.name}"
class CarDashboard(models.Model):
    user_id = models.IntegerField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, default=1)  # Adjust the default value as needed

    def __str__(self):
        return f"Pricing for {self.user_id}"
class CarVideo(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='car_videos/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Video for {self.car.name}"
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    full_name = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.full_name