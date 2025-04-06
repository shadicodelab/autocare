from django import forms
from .models import Garage

class GarageRegistrationForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ['name', 'location', 'services', 'owner_name', 'contact', 'email', 'image']  # Added 'image' field

    # Customize file input
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
