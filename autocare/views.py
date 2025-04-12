from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Garage, GarageLocation, GarageService
from .forms import GarageRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages

@login_required
def register_garage(request):
    if request.method == "POST":
        form = GarageRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            owner_name = form.cleaned_data['owner_name']
            contact = form.cleaned_data['contact']
            email = form.cleaned_data['email']
            image = form.cleaned_data.get('image')

            # Create or get location
            location_address = form.cleaned_data['location_address']
            location_latitude = form.cleaned_data['location_latitude']
            location_longitude = form.cleaned_data['location_longitude']
            location, _ = GarageLocation.objects.get_or_create(
                address=location_address,
                latitude=location_latitude,
                longitude=location_longitude
            )

            # Create the Garage object (without committing services yet)
            garage = Garage.objects.create(
                name=name,
                location=location,
                owner_name=owner_name,
                contact=contact,
                email=email,
                image=image
            )

            # Handle many-to-many services selection from checkboxes
            service_ids = request.POST.getlist('services')  # returns a list of strings
            selected_services = GarageService.objects.filter(id__in=service_ids)
            garage.services.set(selected_services)

            messages.success(request, "Garage registered successfully!")
            return redirect('service')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = GarageRegistrationForm()

    # Manually pass services to render in the template
    services = GarageService.objects.all()

    return render(request, 'autocare/register_garage.html', {
        'form': form,
        'services': services
    })



def services_page_view(request):
    garages = Garage.objects.select_related('location').all()
    return render(request, 'autocare/services.html', {'garages': garages})


@login_required
def search_garages(request):
    location = request.GET.get('location', '').strip()
    service = request.GET.get('service', '').strip()

    all_services = GarageService.objects.all()
    garages = Garage.objects.all()

    if location:
        garages = garages.filter(location__address__icontains=location)

    if service:
        garages = garages.filter(services__name__icontains=service)

    return render(request, 'autocare/service.html', {
        'garages': garages,
        'all_services': all_services,
        'request': request  # to preserve form state
    })


# Create your views here.
def index(request):
    return render(request, "autocare/index.html")

def not_found(request):
    return render(request, "autocare/404.html")

def about(request):
    return render(request, 'autocare/about.html')

def booking(request):
    return render(request,"autocare/booking.html")

def contact(request):
    return render(request, "autocare/contact.html")


@login_required
def service(request):
    location_name = request.GET.get('location', '').strip()
    service_name = request.GET.get('service', '').strip()

    # Fetch all locations and services for the search form
    all_locations = GarageLocation.objects.all()
    all_services = GarageService.objects.all()

    # Start with all garages
    garages = Garage.objects.all()

    # Apply filters only if any search input is provided
    if location_name:
        garages = garages.filter(location__address__icontains=location_name)

    if service_name:
        garages = garages.filter(services__name__icontains=service_name)

    return render(request, "autocare/service.html", {
        'garages': garages,
        'all_services': all_services,
        'all_locations': all_locations,
    })




def team(request):
    return render(request, "autocare/team.html")

def testimonial(request):
    return render(request, "autocare/testimonial.html")

def locate(request):
    return render(request, "autocare/locate.html")

def chat(request):
    return render(request, "autocare/chat.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "autocare/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "autocare/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "autocare/register.html", {
                "message": "Passwords must match."
            })

        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            return render(request, "autocare/register.html", {
                "message": "Email already registered."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "autocare/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "autocare/register.html")
    
def chat_view(request):
    return render(request, 'autocare/chat.html')