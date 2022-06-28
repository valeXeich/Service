from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from djoser.signals import user_registered

from .models import Schedule, Specialist, Service, Location
from .utils import create_time_slots


@receiver(post_save, sender=Schedule)
def post_save_create_time_slots(sender, instance, created, **kwargs):
    """
    When creating a schedule,
    time segments of the day are created for it
    """
    if created:
        create_time_slots(instance)


@receiver(post_save, sender=Schedule)
def post_save_check_second_schedule(sender, instance, created, **kwargs):
    """
    Set boolean to true if this is the second
    schedule for the specialist
    """
    if created:
        specialist = instance.specialist
        schedules = Schedule.objects.filter(
            specialist=specialist, day_of_week=instance.day_of_week
        )
        if len(schedules) == 2:
            instance.is_second_schedule = True
            instance.save()
            schedule = schedules.first()
            schedule.second_schedule = instance
            schedule.save()


@receiver(pre_save, sender=Schedule)
def pre_save_user(sender, instance, **kwargs):
    """
    Clearing old time slots and creating
    new ones when updating the schedule
    """
    if not instance._state.adding:
        instance.time_slots.clear()
        create_time_slots(instance)


@receiver(user_registered)
def create_specialist(user, request, **kwargs):
    """Creating a specialist profile when creating a user"""
    if request.data["status"] == "specialist":
        service = Service.objects.create(
            title=request.data["service_title"], time=request.data["service_time"]
        )
        location = Location.objects.create(street=request.data["location"])
        Specialist.objects.create(user=user, service=service, location=location)

