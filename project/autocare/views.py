from django.shortcuts import render

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

def service(request):
    return render(request, "autocare/service.html")

def team(request):
    return render(request, "autocare/team.html")

def testimonial(request):
    return render(request, "autocare/testimonial.html")

def locate(request):
    return render(request, "autocare/locate.html")

def chat(request):
    return render(request, "autocare/chat.html")