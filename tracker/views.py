import time

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import AlcoholForm, CigaretteForm
from .forms import CustomUserCreationForm
from .serializers import UserSerializer
from django.db.models import Sum
from .models import CustomUser, AlcoholIntake, CigaretteIntake
from datetime import datetime, timedelta
from django.utils import timezone
import threading
from django.http import JsonResponse

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Assign refresh token
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),  # Access access_token using __str__()
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'homepage.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            messages.success(request, f"User {user.username} registered successfully!")  # Debug message
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"User {user.username} logged in successfully!")  # Debug message
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid credentials.")  # Debug message
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    user = request.user
    height = user.height
    weight = user.weight
    phone_number = user.phone_number
    # Get the updated BAC for the current user
    updated_bac = user.bac
    cigarette_toxins = user.cigarette_toxins if hasattr(user, 'cigarette_toxins') else None

    # Calculate total alcohol intake for the user
    total_alcohol = AlcoholIntake.objects.filter(user=user).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Calculate total number of cigarettes smoked by the user
    total_cigarettes = CigaretteIntake.objects.filter(user=user).aggregate(total_units=Sum('units'))['total_units'] or 0

    context = {
        'user': user,
        'height': height,
        'weight': weight,
        'phone_number': phone_number,
        'updated_bac': updated_bac,
        'cigarette_toxins': cigarette_toxins,
        'total_alcohol': total_alcohol,
        'total_cigarettes': total_cigarettes,
    }

    return render(request, 'dashboard.html', context)


def calculate_bac(alcohol_type, alcohol_intake, weight_kg, gender, last_intake_time=None):
    # Calculate total alcohol intake in grams based on type of alcohol
    if alcohol_type == 'BEER':
        alcohol_grams = 10 * alcohol_intake
    elif alcohol_type == 'WINE':
        alcohol_grams = 14 * alcohol_intake
    elif alcohol_type == 'LIQUOR':
        alcohol_grams = 40 * alcohol_intake
    else:
        alcohol_grams = 14 * alcohol_intake
    # Convert weight to grams
    weight_grams = weight_kg * 1000

    # Define distribution ratios
    distribution_ratio = 0.68 if gender == 'M' else 0.55

    # Calculate BAC
    bac = (alcohol_grams / weight_grams) * 100 * distribution_ratio

    # Reduce BAC based on time elapsed since last intake
    if last_intake_time:
        current_time = timezone.now()
        time_elapsed = (current_time - last_intake_time).total_seconds() / 3600
        bac -= time_elapsed * 0.015  # Assume BAC decreases by 0.015 per hour

    return max(bac, 0)


def update_bac_thread():
    while True:
        # Retrieve all users
        users = CustomUser.objects.all()
        print("Updating BAC for all users...")

        # Update BAC for each user
        for user in users:
            last_intake_time = user.alcoholintake_set.last().timestamp if user.alcoholintake_set.exists() else None
            updated_bac = calculate_bac(user.alcohol_type, user.alcohol_intake, user.weight, user.gender,
                                        last_intake_time)
            user.bac = updated_bac
            print(updated_bac)
            user.save()

        # Sleep for some time before updating again
        time.sleep(3600)  # Sleep for 1 hour


def start_bac_update_thread():
    # Create a thread to continuously update the BAC
    bac_update_thread = threading.Thread(target=update_bac_thread)
    bac_update_thread.daemon = True
    bac_update_thread.start()


# Call this function when the server starts
def start_bac_update():
    start_bac_update_thread()





@login_required
def get_updated_bac(request):
    # Fetch the current user
    user = request.user

    # Get the updated BAC for the current user
    updated_bac = user.bac

    # Return the updated BAC value as JSON response
    return JsonResponse({'updated_bac': updated_bac})


def calculate_alcohol_toxins(alcohol_type, amount):
    alcohol_toxins_mapping = {
        'BEER': 0.05,
        'WINE': 0.12,
        'LIQUOR': 0.4,
        'MIXED': 0.2,
    }
    alcohol_toxins = alcohol_toxins_mapping.get(alcohol_type, 0)
    total_alcohol_toxins = alcohol_toxins * amount
    return total_alcohol_toxins


def calculate_cigarette_toxins(cigarette_count):
    cigarette_toxins = 0.05
    total_cigarette_toxins = cigarette_toxins * cigarette_count
    return total_cigarette_toxins


@login_required
def add_drug_intake(request):
    alcohol_form = AlcoholForm()
    cigarette_form = CigaretteForm()

    if request.method == 'POST':
        if 'alcohol_submit' in request.POST:
            alcohol_form = AlcoholForm(request.POST)
            if alcohol_form.is_valid():
                alcohol_intake = alcohol_form.save(commit=False)
                alcohol_intake.user = request.user
                alcohol_intake.save()

                # Update BAC in user profile
                weight_kg = request.user.weight
                gender = request.user.gender
                alcohol_type = alcohol_intake.alcohol_type
                alcohol_amount = alcohol_intake.amount

                bac = calculate_bac(alcohol_type, alcohol_amount, weight_kg, gender, alcohol_intake.timestamp)
                alc_toxin = calculate_alcohol_toxins(alcohol_type, alcohol_amount)
                request.user.bac = bac
                request.user.alcohol_toxins = alc_toxin
                request.user.save()

                # Display a success message
                messages.success(request, f"Alcohol intake recorded successfully!")

                # return redirect('dashboard')

        elif 'cigarette_submit' in request.POST:
            cigarette_form = CigaretteForm(request.POST)
            if cigarette_form.is_valid():
                cigarette_intake = cigarette_form.save(commit=False)
                cigarette_intake.user = request.user
                cigarette_intake.save()

                # Update cigarette toxins in user profile
                cigarette_count = cigarette_intake.units
                cigarette_toxins = calculate_cigarette_toxins(cigarette_count)
                request.user.cigarette_toxins = cigarette_toxins
                request.user.save()

                # Display a browser success message
                messages.success(request, f"Cigarette intake recorded successfully!")

                # return redirect('dashboard')

    context = {
        'alcohol_form': alcohol_form,
        'cigarette_form': cigarette_form,
    }
    return render(request, 'intake.html', context)
