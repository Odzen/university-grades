from django.core.validators import MinValueValidator
from django.db import models
from .choices import SUBJECT_LEVEL_CHOICES
from django.db.models import Q
from users.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number_credits = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    semester = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])

    level = models.CharField(
        choices=SUBJECT_LEVEL_CHOICES,
        max_length=100,
        verbose_name="Subject level",
        default="BACHELOR",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='required_for', blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        max_length=10,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_subjects",
        limit_choices_to=Q(role="ADMIN") | Q(role="USER", type="TEACHER"),
    )

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)