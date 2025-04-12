from django import forms
from .models import Garage, GarageLocation, GarageService
import bleach
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class GarageRegistrationForm(forms.ModelForm):
    # Location fields (not directly in Garage model)
    location_address = forms.CharField(max_length=255, required=True, label="Location Address")
    location_latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=True, label="Latitude")
    location_longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=True, label="Longitude")

    # Render services as checkboxes
    services = forms.ModelMultipleChoiceField(
        queryset=GarageService.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label="Select Services"
    )

    class Meta:
        model = Garage
        fields = ['name', 'owner_name', 'contact', 'email', 'image']

    # Customize file input widget for image
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    
    def clean_name(self):
        name = self.cleaned_data['name']
        return bleach.clean(name)
    
    
    def clean_location(self):
        location = self.cleaned_data['location']
        return bleach.clean(location)
        
    
    def clean_owner_name(self):
        owner_name = self.cleaned_data['owner_name']
        return bleach.clean(owner_name)
    
    
    def clean_contact(self):
        contact = self.cleaned_data['contact']
        return bleach.clean(contact)
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email format.")
        return bleach.clean(email)
    
