
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import dept
from .models import doctors as Doctor
from .forms import BookingForm, ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .recommendations import recommend_doctors, find_specializations


def index(request):
    return render(request, "index.html")

@login_required
def about(request):
    context = {
        'experience': '15 years',
    }
    return render(request, "about.html", context)

@login_required
def contact(request):
    context = {
        'instagram': 'adhiii.ig',
        'whatsapp': '+91 7012 345 678',
    }
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent. We’ll be in touch soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    context['form'] = form
    return render(request, 'contact.html', context)

@login_required
def doctors(request):
    doctor_list = Doctor.objects.select_related('dept_name').all()
    context = {
        'doctors': doctor_list,
    }
    return render(request, "doctors.html", context)

@login_required
def departments(request):
    departments = {
        'departments': dept.objects.all()
    }
    return render(request, "departments.html", departments)
from django.http import HttpResponse
@login_required
def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})
def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("index")
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{'form': form}) 

@login_required
def smart_recommendation(request):
    doctors = []
    symptoms = ""
    searched = False

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        searched = True

        if symptoms:
            doctors = recommend_doctors(symptoms)

    return render(
        request,
        "smart_recommendation.html",
        {
            "doctors": doctors,
            "symptoms": symptoms,
            "searched": searched,
        },
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import (
    UserProfile,
    booking as Booking,
    contact as Contact,
    dept as Department,
)
from .forms import AdminProfileForm, ProfileForm

@login_required
def profile(request):

    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.user.is_superuser or request.user.is_staff:
        user_profile.role = 'admin'
        user_profile.save()

    if request.method == 'POST':
        form_class = (
            AdminProfileForm
            if user_profile.role == 'admin'
            else ProfileForm
        )
        form = form_class(
            request.POST,
            request.FILES,
            instance=user_profile,
            user=request.user
        )

        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            form.save()
            return redirect('profile')

    else:
        form_class = (
            AdminProfileForm
            if user_profile.role == 'admin'
            else ProfileForm
        )
        form = form_class(
            instance=user_profile,
            user=request.user
        )

    template = (
        'admin_profile.html'
        if user_profile.role == 'admin'
        else 'patient_profile.html'
    )

    context = {
        'form': form,
        'profile': user_profile,
    }
    if user_profile.role == 'admin':
        context['admin_stats'] = {
            'doctors': Doctor.objects.count(),
            'departments': Department.objects.count(),
            'appointments': Booking.objects.count(),
            'messages': Contact.objects.count(),
        }

    return render(request, template, context)