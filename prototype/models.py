from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import forms
# Create your models here.

class userManager(BaseUserManager):
    def create_user(self, first_name, last_name, user_type, email, password):
        if not email:
            raise ValueError("Users must have an email address.")
        if not first_name:
            raise ValueError("Users must have a first name.")
        if not last_name:
            raise ValueError("Users must have a last name.")
        if not user_type:
            raise ValueError("Users must have type.")
        user = self.model(
            email=self.normalize_email(email), first_name=first_name, last_name=last_name, user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, user_type, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Skill(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'

class User(AbstractBaseUser):

    USER_TYPE_CHOICES = (
        ("ME", "Mentee"),
        ("MO", "Mentor"),
        ("SU", "Super User")
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length = 2,
        choices = USER_TYPE_CHOICES,
        default = 'ME'
        )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill)

    objects = userManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "user_type"]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


