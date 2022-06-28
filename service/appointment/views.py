from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, views
from rest_framework.response import Response

from .models import (Appointment, Location, MyUser, Schedule, Service,
                     Specialist, TimeSlots)
from .permissions import IsClient, IsSpecialistOwnerOrAdmin
from .serializers import (AppointmentCreateSerializer, AppointmentSerializer,
                          LocationSerializer, ScheduleInfoSerializer,
                          ScheduleSerializer, ScheduleUpdateSerializer,
                          ServiceSerializer, SpecialistScheduleSerializer,
                          SpecialistSerializer, UserSerializer)
from .tasks import delete_appointment
from .utils import get_difference_between_dates, get_work_date


class SpecialistListApiView(generics.ListAPIView):
    """Get list of specialists"""

    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["service"]
    permission_classes = [permissions.AllowAny]


class SpecialistScheduleListApiView(generics.ListAPIView):
    """Get list specialist schedules"""

    queryset = Schedule.objects.all()
    serializer_class = SpecialistScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date"]


class SpecialistDetailScheduleListApiView(generics.ListAPIView):
    """Get specialist schedules by slug"""

    serializer_class = ScheduleInfoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        specialist = Specialist.objects.get(user__slug=self.kwargs["slug"])
        schedule = Schedule.objects.filter(specialist=specialist)
        return schedule


class SpecialistAppointmentListApiView(generics.ListAPIView):
    """Get list appointment by specialist"""

    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date"]
    permission_classes = [IsSpecialistOwnerOrAdmin]

    def get_queryset(self):
        specialist = Specialist.objects.get(user__slug=self.kwargs["slug"])
        return Appointment.objects.filter(specialist=specialist)


class ScheduleCreateApiView(generics.CreateAPIView):
    """Create schedule"""

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsSpecialistOwnerOrAdmin]

    def perform_create(self, serializer):
        if "specialist" not in self.request.data:
            specialist = self.request.user.specialist_set.all().first()
            return serializer.save(specialist=specialist)
        return serializer.save()


class UserInfoRetrieveApiView(generics.RetrieveAPIView):
    """Get info about user"""

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated]


class ScheduleUpdateApiView(generics.UpdateAPIView):
    """Update schedule"""

    queryset = Schedule.objects.all()
    serializer_class = ScheduleUpdateSerializer
    permission_classes = [IsSpecialistOwnerOrAdmin]


class ScheduleDeleteApiView(generics.DestroyAPIView):
    """Delete schedule"""

    queryset = Schedule.objects.all()
    permission_classes = [IsSpecialistOwnerOrAdmin]


class ServiceListApiView(generics.ListAPIView):
    """Get list of service"""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class AppointmentCreateApiView(generics.CreateAPIView):
    """Create appointment"""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsClient]

    def perform_create(self, serializer):
        date = self.request.data["date"]
        specialist = self.request.data["specialist"]
        time_slot_pk = self.request.data["time_slot"]
        time_slot = TimeSlots.objects.get(pk=time_slot_pk)
        schedule = Schedule.objects.get(
            specialist=specialist, time_slots__in=[time_slot]
        )
        schedule.time_slots.remove(time_slot)
        seconds = get_difference_between_dates(date, time_slot_pk)
        delete_appointment.apply_async(
            (
                self.request.user.id,
                specialist,
                date,
                time_slot_pk,
                schedule.id,
            ),
            countdown=seconds,
        )
        return serializer.save(client=self.request.user)


class ClientAppointmentListApi(generics.ListAPIView):
    """Get list appointment for client"""

    serializer_class = AppointmentSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user)


class LocationListApiView(generics.ListAPIView):
    """Get list of location"""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]


class DateAndTimeWorkApiView(views.APIView):
    """Get time slots for date"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk, format=None):
        specialist = Specialist.objects.get(pk=pk)
        dates = get_work_date(specialist)
        return Response(dates)
