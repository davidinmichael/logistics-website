from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.views import View


class LoginView(View):
    def get(self, request):
        return render(request, "account/login.html")

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("view_shipments")
            else:
                messages.error(request, "Invalid email or password.")
        messages.error(request, "Invalid form details")
        return render(request, "account/login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "account/register.html")

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("view_shipments")
        messages.error(request, "Invalid form details")
        print(f"{form.errors}")
        return render(request, "account/register.html")
