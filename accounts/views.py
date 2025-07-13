from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm, AuthenticationForm
from .models import User


@method_decorator([csrf_protect, never_cache], name="dispatch")
class RegisterView(CreateView):
    """
    Class-based view for user registration.
    """
    model = User
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are already logged in."))
            return redirect("dashboard:dashboard")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                
                # Auto-login after registration (optional)
                login(self.request, self.object)
                
                messages.success(
                    self.request,
                    _("Welcome! Your account has been created successfully.")
                )
                
                return response
                
        except Exception as e:
            messages.error(
                self.request,
                _("An error occurred during registration. Please try again.")
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _("Please correct the errors below."))
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": _("Create Account"),
            "submit_text": _("Register"),
        })
        return context
    
    
class LoginView(DjangoLoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True