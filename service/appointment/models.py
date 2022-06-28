from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    STATUS = (("specialist", "Специалист"), ("client", "Клиент"))
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(max_length=20)

    def save(self, *args, **kwargs):
        self.slug = self.username
        super().save(*args, **kwargs)


class Location(models.Model):
    street = models.CharField(max_length=50)

    def __str__(self):
        return self.street


class Service(models.Model):
    title = models.CharField(max_length=50)
    time = models.TimeField()

    def __str__(self):
        return self.title


class Specialist(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="specialists"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="specialists"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}: {self.service}"


class TimeSlots(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"{self.start} : {self.end}"


class Schedule(models.Model):

    DAYS_OF_WEEK = (
        ("monday", "Понедельник"),
        ("tuesday", "Вторник"),
        ("wednesday", "Среда"),
        ("thursday", "Четверг"),
        ("friday", "Пятница"),
        ("saturday", "Суббота"),
        ("sunday", "Воскресенье"),
    )

    day_of_week = models.CharField(
        max_length=20, choices=DAYS_OF_WEEK, default="monday"
    )
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE, related_name="schedules", null=True
    )
    start_schedule = models.TimeField()
    end_schedule = models.TimeField()
    second_schedule = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    is_second_schedule = models.BooleanField(default=False)
    time_slots = models.ManyToManyField(TimeSlots)

    def __str__(self):
        return f"{self.day_of_week} {self.start_schedule} - {self.end_schedule}"


class Appointment(models.Model):
    client = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE, related_name="appointments"
    )
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE)

    def __str__(self):
        return f"client: {self.client.username}, specialist: {self.specialist.user.username}"
