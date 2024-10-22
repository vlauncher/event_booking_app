# users/views.py

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from allauth.account.views import (
    SignupView as DefaultSignupView,
    LoginView as DefaultLoginView,
    LogoutView as DefaultLogoutView,
    PasswordChangeView 
)
from django.contrib.auth.views import LoginView
from django.contrib import messages  # Import the messages framework
from .forms import CustomLoginForm, CustomPasswordChangeForm


# Custom Signup View
class SignupView(DefaultSignupView):
    template_name = 'signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Registration successful! Please log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors below.")
        return super().form_invalid(form)


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your custom template

    def form_valid(self, form):
        messages.success(self.request, "Login successful! Welcome back.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Login failed. Please check your email and password.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Add custom context to the template."""
        context = super().get_context_data(**kwargs)
        return context


# Custom Change Password View
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'changepassword.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')  # Redirect to home on success

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Password change failed. Please correct the errors below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# Custom Logout View
class LogoutView(DefaultLogoutView):
    template_name = 'logout.html'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


# Home View
class HomeView(TemplateView):
    template_name = 'home.html'


# users/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from .forms import UserProfileUpdateForm
from .models import Profile

class ListProfileView(View):
    template_name = 'list_profile.html'

    def get(self, request):
        user_profile = get_object_or_404(Profile, user=request.user)
        context = {
            'profile': user_profile
        }
        return render(request, self.template_name, context)


class UpdateProfileView(View):
    template_name = 'update_profile.html'

    def get(self, request):
        user_profile = get_object_or_404(Profile, user=request.user)
        form = UserProfileUpdateForm(instance=user_profile)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_profile = get_object_or_404(Profile, user=request.user)
        form = UserProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('list_profile')  # Redirect to the profile list after updating
        messages.error(request, "Failed to update profile. Please correct the errors below.")
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
