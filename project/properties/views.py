from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Property, Contact, Booking  # Ensure models are imported

# ✅ Home Page
def index(request):
    return render(request, 'properties/index.html')

# ✅ Property List
def property_list(request):
    rent_properties = Property.objects.filter(property_type='Rent')
    buy_properties = Property.objects.filter(property_type='Buy')
    return render(request, 'properties/index.html', {
        'rent_properties': rent_properties,
        'buy_properties': buy_properties
    })

# ✅ Post Property
def post_property(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        property_type = request.POST.get('property_type')
        image = request.FILES.get('image')

        contact_name = request.POST.get('contact_name')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')

        property_instance = Property.objects.create(
            name=name,
            location=location,
            price=price,
            bedrooms=bedrooms,
            property_type=property_type,
            image=image  
        )

        Contact.objects.create(
            property=property_instance,
            name=contact_name,
            phone=contact_phone,
            email=contact_email
        )

        return redirect('property_list')

    return render(request, 'properties/post_property.html')

# ✅ Property Detail
def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    return render(request, 'properties/property_detail.html', {'property': property_obj})

# ✅ Booking Function (Redirect to Confirm Booking)
def book_now(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to book a property.")
            return redirect('login')

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # ✅ Debugging print
        print(" Received Booking Request:", request.POST)

        if not start_date or not end_date:
            messages.error(request, "Please select both start and end dates.")
            return redirect('book_now', property_id=property_id)

        try:
                booking = Booking.objects.create(
                      property=property_obj,
                      user=request.user,
                      date=booking_date
)
booking.save()  # Ensure booking is saved

# Debugging: Print Booking ID
print(f"✅ Booking Created! ID: {booking.id}")  

# Redirect to Confirm Booking Page
return HttpResponseRedirect(reverse('confirm_booking', args=[booking.id]))
#  Confirm Booking (Redirect to Signup Page)
def confirm_booking(request, booking_id):
    
    booking = get_object_or_404(Booking, id=booking_id)

    
    booking.status = "Confirmed"
    booking.save()

    # Debugging print to check if function is working
    print(f" Redirecting to Signup/Login Page...")  # Debugging print

    #  Redirect to Signup Page
    if not request.user.is_authenticated:
      return redirect('signup')

#If user is authenticated, redirect to login page
    return redirect('login')
#  Agreement Page Function
def agreement_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'properties/agreement.html', {'booking': booking})

#  Get Contact Details
def get_contact_details(request, property_id):
    try:
        contact = Contact.objects.get(property_id=property_id)
        return JsonResponse({
            'success': True,
            'name': contact.name,
            'phone': contact.phone,
            'email': contact.email
        })
    except Contact.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Contact details not found'})

#  User Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect('index')

    return render(request, 'accounts/signup.html')

#  User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')

#  User Logout (Add This at the Bottom)
def logout_view(request):
    logout(request)
    return redirect('index')
