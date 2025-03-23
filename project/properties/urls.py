from django.urls import path
from properties.views import book_now, confirm_booking
from . import views

urlpatterns = [
    #  Home and Property Routes
    path('', views.property_list, name='property_list'),
    path('post-property/', views.post_property, name='post_property'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),

    #  Authentication URLs
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    #  Contact and Booking
    path('contact/<int:property_id>/', views.get_contact_details, name='get_contact_details'),
    path('book_now/<int:property_id>/', views.book_now, name='book_now'),
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('agreement/<int:booking_id>/', views.agreement_page, name='agreement_page'),

    #  Payment Page Route (Uncomment if needed)
    # path('payment/<int:booking_id>/', views.payment_page, name='payment'),
]
