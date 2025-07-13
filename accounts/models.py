from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from .utils import *


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model where email is the unique identifier.
    """
    
    GENDER_CHOICES = [
        ("M", _("Male")),
        ("F", _("Female")),
    ]


    email = models.EmailField(
        _("email address"), 
        unique=True, 
        max_length=255
    )
    
    first_name = models.CharField(
        _("first name"), 
        max_length=30, 
        blank=True
    )
    
    last_name = models.CharField(
        _("last name"), 
        max_length=30, 
        blank=True
    )
    
    gender = models.CharField(
        _("gender"),
        max_length=2,
        choices=GENDER_CHOICES,
        blank=True,
        help_text=_("User's gender."),
    )
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    
    date_joined = models.DateTimeField(
        _("date joined"), 
        default=now
    )
    
    avatar = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to=upload_avatar_to,
        blank=True,
        validators=[validate_avatar],
        help_text=_("Upload a profile picture (max 2MB, JPG/PNG only)")
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name of the user."""
        return self.first_name