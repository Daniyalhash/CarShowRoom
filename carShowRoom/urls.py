from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static  # Fix the import statement
urlpatterns = [
    path('', Signup, name='myview'),
    path('myview/', myview, name='myview'),
    path('Login/', Login, name='Login'),
    path('Signup/', Signup, name='Signup'),
    path('Logout/', Logout, name='Logout'),
    path('add_car/', add_car, name='add_car'),

    path('search/', search, name='search'),
    path('delete_car-us/<int:car_dashboard_id>', delete_car, name='delete_car'),
    path('message-us/', message_us, name='message_us'),
    path('AdminPanel/', AdminPanel, name='AdminPanel'),
    path('AdminLogin/', AdminLogin, name='AdminLogin'),
    path('AdminPage/', AdminPage, name='AdminPage'),
    path('delete_car_db/', delete_car_db, name='delete_car_db'),
    path('update_car/', update_car, name='update_car'),

    path('Contact/', Contact, name='Contact'),
    path('About/', About, name='About'),
    path('like/', like, name='like'),
    path('add_to_whislist/<int:car_id>/', add_to_whislist, name='add_to_whislist'),
    path('remove_from_wishlist/<int:id>/', remove_from_wishlist, name='remove_from_wishlist'),

    # path('send_email/', send_email, name='send_email'),
    path('search_update_car/', search_update_car, name='search_update_car'),
    path('view-cars/', view_cars, name='view_cars'),

    path('Shop/', Shop, name='Shop'),
    path('Dashboard/', Dashboard, name='Dashboard'),
    path('Payment/<int:car_id>/<int:user_id>/', Payment, name='Payment'),
    path('Product/<int:id>/', Product, name='Product'),  
    path('save_data/', save_data, name='save_data'),
  path('Celebration/<int:car_id>/<int:color_id>/<int:user_id>/', Celebration, name='Celebration'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Fix the variable name
