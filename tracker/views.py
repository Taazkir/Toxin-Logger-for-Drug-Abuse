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
    return render(request, 'dashboard.html', {'user': request.user})


def calculate_bac(alcohol_grams, weight_kg, gender):
    # Convert weight to grams
    weight_grams = weight_kg * 1000

    # Define distribution ratios
    distribution_ratio = 0.68 if gender == 'M' else 0.55

    # Calculate BAC
    bac = (alcohol_grams / weight_grams) * 100 * distribution_ratio

    return bac


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
                return redirect('dashboard')
        elif 'cigarette_submit' in request.POST:
            cigarette_form = CigaretteForm(request.POST)
            if cigarette_form.is_valid():
                cigarette_intake = cigarette_form.save(commit=False)
                cigarette_intake.user = request.user
                cigarette_intake.save()
                return redirect('dashboard')
    return render(request, 'intake.html',
                  {'alcohol_form': alcohol_form, 'cigarette_form': cigarette_form})
