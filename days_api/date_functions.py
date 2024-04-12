"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """ Converts date into datetime """
    try:
        date_object = datetime.strptime(date_val, "%d.%m.%Y")
        return date_object
    except:
        raise ValueError("Unable to convert value to datetime.")


def get_days_between(first: datetime, last: datetime) -> int:
    """ Returns how many days between 2 given datetimes """
    if isinstance(first, datetime) and isinstance(last, datetime):
        return (last-first).days
    else:
        raise TypeError("Datetimes required.")


def get_day_of_week_on(date_val: datetime) -> str:
    """ Returns day of the week from date """
    if isinstance(date_val, datetime):
        return date_val.strftime('%A')
    else:
        raise TypeError("Datetime required.")


def get_current_age(birthdate: date) -> int:
    """ Computes age from birthdate """
    if isinstance(birthdate, date):
        today = datetime.today()
        # print(today)
        age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))
        print(f'Your age is {age}')
        return age
    else:
        raise TypeError("Date required.")
