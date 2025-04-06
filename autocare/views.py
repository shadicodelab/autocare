from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Garage
from .forms import GarageRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def register_garage(request):
    if request.method == "POST":
        form = GarageRegistrationForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            form.save()
            return redirect('service')  # Redirect to the services page after successful registration
    else:
        form = GarageRegistrationForm()

    return render(request, 'autocare/register_garage.html', {'form': form})

@login_required
def search_garages(request):
    location = request.GET.get('location', '')
    service = request.GET.get('service', '')

    # Fetch all unique services at all times
    all_services = set()
    for garage in Garage.objects.all():
        for srv in garage.services.split(','):
            all_services.add(srv.strip())

    # Filter garages based on user input
    garages = Garage.objects.all()
    if location:
        garages = garages.filter(location__icontains=location)
    if service:
        garages = garages.filter(services__icontains=service)

    return render(request, 'autocare/service.html', {
        'garages': garages,  # Only filters if search is performed
        'all_services': sorted(all_services)  # Services always available
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
    # Fetch all unique services from the database
    all_services = set()
    for garage in Garage.objects.all():
        for srv in garage.services.split(','):
            all_services.add(srv.strip())

    return render(request, "autocare/service.html", {
        'all_services': sorted(all_services)  # Ensure services are listed alphabetically
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