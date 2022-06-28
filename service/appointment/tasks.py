from config.celery import app

from .models import Appointment, Schedule


@app.task
def delete_appointment(client_id, specialist_id, date, time_slot_id, schedule_id):
    """ " Delete appointment after the end of time"""
    appointment = Appointment.objects.get(
        client=client_id, specialist=specialist_id, date=date, time_slot=time_slot_id
    )
    appointment.delete()
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.time_slots.add(time_slot_id)

