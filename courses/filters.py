from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters

from .models import Course


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = ['status', 'teacher', 'created_by', 'subject']


class CourseSearchFilter(drf_filters.SearchFilter):
    search_param = 'search'
    search_fields = ['name']


class CourseOrderingFilter(drf_filters.OrderingFilter):
    ordering_param = 'ordering'
    ordering_fields = ['name', 'created_at', 'updated_at', 'start_date', 'end_date']
