import calendar
from datetime import date, datetime, timedelta

from .models import Schedule, TimeSlots
from .serializers import TimeSlotSerialize


def correct_time_slot_today(data):
    """Removing irrelevant time segments for today"""
    queryset_to_list = list(data)
    correct_time_slots = []
    for time_slot in queryset_to_list:
        now_time = datetime.today().time()
        if time_slot.start >= now_time:
            correct_time_slots.append(time_slot)
    return correct_time_slots


def get_work_date(specialist):
    """Get dates by day of the week from the schedule (for 7 days)"""
    today = datetime.today().date()
    seven_days = []
    dates = {}
    schedules = Schedule.objects.filter(specialist=specialist)
    seven_days.append(today)
    for i in range(7):
        today += timedelta(days=1)
        seven_days.append(today)
    for schedule in schedules:
        for date in seven_days:
            if schedule.day_of_week == calendar.day_name[date.weekday()].lower():
                data = schedule.time_slots.all().order_by("start")
                if date.day == datetime.today().day:
                    correct_queryset = correct_time_slot_today(data)
                    dates[date.isoformat()] = TimeSlotSerialize(
                        correct_queryset, many=True
                    ).data
                else:
                    dates[date.isoformat()] = TimeSlotSerialize(data, many=True).data
        if len(dates) == len(schedules):
            break
    return dates


def get_difference_between_dates(date, time_slot_pk):
    """Get the difference in seconds between dates"""
    time_slot = TimeSlots.objects.get(pk=time_slot_pk)
    end_time_slot = str(time_slot.end).replace(":", "-")
    full_time = date + "-" + end_time_slot
    convert_to_datetime = datetime.strptime(full_time, "%Y-%m-%d-%H-%M-%S")
    now = datetime.today()
    seconds = int((convert_to_datetime - now).total_seconds())
    return seconds


def create_time_slots(instance):
    """
    Creation of time segments at the beginning of the schedule
    and the end are separated by the time duration of the service
    """
    specialist = instance.specialist
    time_service = specialist.service.time
    start_schedule = instance.start_schedule
    end_schedule = instance.end_schedule
    seconds = (time_service.hour * 60 + time_service.minute) * 60 + time_service.second
    instance.time_slots.get_or_create(
        start=start_schedule,
        end=(
            datetime.combine(date.today(), start_schedule) + timedelta(seconds=seconds)
        ).time(),
    )
    while True:
        last_time = instance.time_slots.all().last().end
        next_time = (
            datetime.combine(date.today(), last_time) + timedelta(seconds=seconds)
        ).time()
        instance.time_slots.get_or_create(start=last_time, end=next_time)
        if next_time.__str__() == end_schedule.__str__():
            break

