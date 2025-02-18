from datetime import date, time, datetime
from .deactivation import booking, date as d, time as t
from .reminders import reminder


class TaskManager:
    class Deactivation:

        @staticmethod
        async def booking(booking_id: int, date: date, time: time):
            await booking.schedule_deactivate_booking(booking_id, date, time)

        @staticmethod
        async def date(date_id: int, deactivate_time: datetime):
            await d.schedule_deactivate_date(date_id, deactivate_time)

        @staticmethod
        async def time(time_id: int, date: date, time: time):
            await t.schedule_deactivate_time(time_id, date, time)

    class Reminders:
        @staticmethod
        async def reminder(chat_id: int, reminder_time: datetime, message: str):
            await reminder.schedule_reminder(chat_id, reminder_time, message)
