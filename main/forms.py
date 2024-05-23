from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'plane_number', 'departure', 'arrival', 
                  'depart_time', 'arrive_time', 'total_seats']
        widgets = {
            'depart_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input', 
                'data-target': '#depart_time_picker'
            }),
            'arrive_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input', 
                'data-target': '#arrive_time_picker'
            }),
        }

class FlightEdit(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'plane_number', 'departure', 'arrival', 
                  'depart_time', 'arrive_time', 'total_seats']
        widgets = {
            'depart_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input', 
                'data-target': '#depart_time_picker'
            }),
            'arrive_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input', 
                'data-target': '#arrive_time_picker'
            }),
        }
