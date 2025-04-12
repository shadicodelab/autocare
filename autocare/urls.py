from django.urls import path



from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("about", views.about, name="about"),
    path("booking", views.booking, name="booking"),
    path("contact",views.contact, name="contact"),
    path("service", views.service, name="service"),
    path("team", views.team, name="team"),
    path("testimonial", views.testimonial, name="testimonial"),
    path("404", views.not_found, name="404"),
    path("locate", views.locate, name="locate"),
    path("chat", views.chat, name="chat"),
    path('register-garage', views.register_garage, name='register_garage'),
    path('search-garages', views.search_garages, name='search_garages'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('chat/', views.chat, name='chat'), # WebSocket connection

    ]

# Serve media files in development mode
