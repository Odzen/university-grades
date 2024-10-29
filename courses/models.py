from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from subjects.models import Subject
from users.models import User
from .choices import COURSE_STATUS_CHOICES


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    status = models.CharField(
        choices=COURSE_STATUS_CHOICES,
        max_length=100,
        verbose_name="Course status",
        default="CREATED",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
    )
    teacher = models.ForeignKey(
        User,
        max_length=10,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_courses",
    )
    enrollments = models.ManyToManyField(
        User, max_length=10, through="Enrollment", related_name="courses"
    )
    created_by = models.ForeignKey(
        User,
        max_length=10,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_courses",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    overall_grade = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.email} enrolled in {self.course.name}"
