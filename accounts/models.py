from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from accounts.generic_model import GenericModel


# Create your models here.
class UserManager(BaseUserManager):
    """Extends Base User Manager to implement user managers"""

    def create_user(
        self, first_name, last_name, username, email, password=None
    ):
        """Creates a user"""
        if not email:
            raise ValueError("User cannot exist without an email!")

        if not username:
            raise ValueError("User cannot exist without an username!")

        if not password:
            raise ValueError("Password cannot be empty")

        user = self.model(
            email=self.normalize_email(email=email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, username, email, password=None
    ):
        """Creates a superuser"""
        user = self.create_user(
            first_name, last_name, username, email, password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_super_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Defines the user model for foodline's users"""

    CUSTOMER = 1
    RESTAURANT = 2

    ROLE_CHOICES = (
        (RESTAURANT, "Restaurant"),
        (CUSTOMER, "Customer"),
    )

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=20)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True
    )

    # required fields
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(GenericModel):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    profile_picture = models.ImageField(
        upload_to="users/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photo", blank=True, null=True
    )
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.email
