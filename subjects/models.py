from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .choices import SUBJECT_LEVEL_CHOICES
from users.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)
    number_credits = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    semester = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    program = models.CharField(max_length=100)

    level = models.CharField(
        choices=SUBJECT_LEVEL_CHOICES,
        max_length=100,
        verbose_name="Subject level",
        default="BACHELOR",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prerequisites = models.ManyToManyField(
        "self", symmetrical=False, related_name="required_for", blank=True
    )

    created_by = models.ForeignKey(
        User,
        max_length=10,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_subjects"
    )

    class Meta:
        ordering = ["-created_at", "name"]
        unique_together = ('name', 'program', 'level')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
