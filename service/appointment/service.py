from django_filters import rest_framework as filters

from .models import Specialist


class SpecialistFilter(filters.FilterSet):
    service = filters.CharFilter(field_name='service__title')

    class Meta:
        model = Specialist
        fields = ['service']
