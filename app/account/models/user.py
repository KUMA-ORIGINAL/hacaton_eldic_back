from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier for authentication."""

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # убираем username
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[EmailValidator(_("Enter a valid email address."))]
    )
    full_name = models.CharField(_("ФИО"), max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} - {self.full_name}"
