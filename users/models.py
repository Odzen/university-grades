import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import USER_ROLE_CHOICES, USER_TYPE_CHOICES


class User(AbstractUser):
    email = models.EmailField(verbose_name="Email address", unique=True)
    username = None

    role = models.CharField(
        choices=USER_ROLE_CHOICES,
        max_length=100,
        verbose_name="User role",
        default="USER",
    )

    type = models.CharField(
        choices=USER_TYPE_CHOICES,
        max_length=100,
        verbose_name="User type",
        default="STUDENT",
    )

    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):

        if not self.username:
            self.username = "".join(
                random.choice(string.ascii_lowercase + string.digits) for _ in range(30)
            )

        super(User, self).save(*args, **kwargs)
