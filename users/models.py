import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import USER_ROLE_CHOICES, USER_TYPE_CHOICES
from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(verbose_name="Email address", unique=True)

    updated_at = models.DateTimeField(auto_now=True)

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
        blank=True,
        limit_choices_to={"type": "ADMIN"},
    )

    objects = UserManager()

    class Meta:
        swappable = "AUTH_USER_MODEL"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):

        if not self.username:
            self.username = "".join(
                random.choice(string.ascii_lowercase + string.digits) for _ in range(30)
            )

        if not self.pk and self._state.adding:
            if hasattr(kwargs, "request"):
                self.created_by = kwargs["request"].user

        super(User, self).save(*args, **kwargs)
