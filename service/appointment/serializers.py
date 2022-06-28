from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from .models import (Appointment, Location, MyUser, Schedule, Service,
                     Specialist, TimeSlots)


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ["status", "password", "username", "first_name", "last_name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "slug",
            "id",
            "status",
            "specialist_set",
            "is_staff",
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "day_of_week",
            "start_schedule",
            "end_schedule",
            "is_second_schedule",
            "specialist",
            "id",
        ]

    def validate(self, data):
        if data["end_schedule"] < data["start_schedule"]:
            raise serializers.ValidationError(
                {"time": "end_schedule less than start_schedule"}
            )
        if "specialist" in data:
            schedule = Schedule.objects.filter(
                specialist=data["specialist"], day_of_week=data["day_of_week"]
            ).first()
            if schedule.end_schedule > data["start_schedule"]:
                raise serializers.ValidationError(
                    {"time": "parent end_schedule bigger than children start_schedule"}
                )
        if "specialist" in data:
            schedule = Schedule.objects.filter(
                specialist=data["specialist"], day_of_week=data["day_of_week"]
            )
            if len(schedule) == 2:
                raise serializers.ValidationError(
                    {"time": "you have already set the time"}
                )
        return data


class ScheduleInfoSerializer(serializers.ModelSerializer):
    day_of_week = serializers.CharField(source="get_day_of_week_display")
    second_schedule = ScheduleSerializer()

    class Meta:
        model = Schedule
        fields = [
            "day_of_week",
            "start_schedule",
            "end_schedule",
            "second_schedule",
            "is_second_schedule",
            "id",
        ]


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["start_schedule", "end_schedule"]


class SpecialistSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    service = serializers.SlugRelatedField(slug_field="title", read_only=True)
    location = serializers.SlugRelatedField(slug_field="street", read_only=True)
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = Specialist
        fields = "__all__"


class SpecialistScheduleInfoSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(slug_field="title", read_only=True)
    location = serializers.SlugRelatedField(slug_field="street", read_only=True)

    class Meta:
        model = Specialist
        exclude = ["user", "schedule"]


class SpecialistScheduleSerializer(serializers.ModelSerializer):
    specialists = SpecialistScheduleInfoSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ["date", "specialists"]


class SpecialistInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    service = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = Specialist
        fields = ["service", "user"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["title", "id"]


class TimeSlotSerialize(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = ["id", "start", "end"]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["date", "time_slot", "specialist"]


class AppointmentSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerialize()
    specialist = SpecialistInfoSerializer()
    client = UserSerializer()

    class Meta:
        model = Appointment
        fields = ["time_slot", "specialist", "date", "client"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["street", "id"]

