from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import date

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, phone_number, password=None, **extra_fields):
        if not name:
            raise ValueError('The Name field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.user_permissions.filter(codename=perm).exists()

    def has_perms(self, perms, obj=None):
        return all(self.has_perm(perm) for perm in perms)

    def has_module_perms(self, app_label):
        return self.is_superuser or self.user_permissions.filter(content_type__app_label=app_label).exists()
