from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model.
    """
    
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        SALES_EXECUTIVE = "SALES_EXECUTIVE", "Sales Executive"
        SALES_MANAGER = "SALES_MANAGER", "Sales Manager"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SALES_EXECUTIVE,
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.get_full_name() or self.username
