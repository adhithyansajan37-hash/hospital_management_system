from django import forms
from .models import booking, contact, UserProfile
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    class Meta:
        model = booking
        fields = ['patient_name', 'patient_phone', 'patient_email', 'doctor_name', 'booked_on']
        labels = {
            'patient_name': 'Patient Name',
            'patient_phone': 'patient phone',
            'patient_email': 'Patient Email',
            'doctor_name': 'Doctor Name',
            'booked_on': 'Booked On'}
        widgets={
            'patient_name': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
            'patient_email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
            'patient_phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'}),
            'booked_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doctor_name': forms.Select(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name', 'email', 'phone', 'address', 'subject', 'message']
        labels = {
            'name': 'Your name',
            'email': 'Email address',
            'phone': 'Phone number (optional)',
            'address': 'Current address (optional)',
            'subject': 'Subject',
            'message': 'How can we help?',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-control',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control',
                'autocomplete': 'email',
            }),
            'phone': forms.TelInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control',
                'autocomplete': 'tel',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'What is your message about?',
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Enter your current address',
                'class': 'form-control',
                'autocomplete': 'street-address',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message here',
                'class': 'form-control',
                'rows': 5,
            }),
        }

class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'address',
            'date_of_birth',
            'gender',
            'blood_group',
            'emergency_contact',
            'profile_image'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email


class AdminProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        fields = [
            'phone',
            'address',
            'profile_image',
        ]