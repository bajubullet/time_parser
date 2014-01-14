"""This module contains functions for parsing datetime from string.

It parses date range from string and checks whether given datetime object lies
in the parsed date range.

EXAMPLE STRINGS:
- every fri date: 1/1/2014-10/1/2014 time 4:00 AM-7:00 PM
- every mon time: 3:00 PM-5:00 PM
- every day time: 3:00 PM-5:00 PM
- every weekday time: 3:00 PM-5:00 PM
- every weekend time: 3:00 PM-5:00 PM
- date: 1/1/2014-10/1/2014 time: 8:00 AM-4:30 PM
"""
import datetime
import re


# Regex for parsing period from a string. It accepts following format:
# "every mon|tue|wed|thu|fri|sat|sun|day|weekday|weekend"
# e.g. "every mon" or "every weekday" etc.
_PERIOD_REGEX = re.compile(
    r'every ([mon|tue|wed|thu|fri|sat|sun|day|weekday|weekend]+)')

# Regex for parsing date from a string. It accepts following format:
# "date: dd/mm/yyyy(start date)-dd/mm/yyyy(optional end date)"
# e.g. "date: 10/1/2014-15/1/2014" or "date: 13/1/2014" etc.
_DATE_REGEX = re.compile(
    r'date: (\d{1,2}/\d{1,2}/\d{1,4})-?(\d{1,2}/\d{1,2}/\d{1,4})?')

# Regex for parsing time from a string. It accepts following format:
# "time: hh:mm AM|PM(start time)-hh:mm AM|PM(optional end time)"
# e.g. "time: 8:00 AM-4:30 PM" or "time: 11:11 AM" etc.
_TIME_REGEX = re.compile(
    r'time: (\d{1,2}:\d{1,2} [A|P]M)-?(\d{1,2}:\d{1,2} [A|P]M)?')

# Weekend days Sat and Sun.
_WEEKEND_DAYS = frozenset([5, 6])


class ParseError(Exception):
  pass


def _ParsePeriod(date_time, string):
  """Checks whether the datetime object exists in given period.

  Parses string to get period and checks whether the datetime object exists in
  given period.

  Args:
    date_time: The datetime object.
    string: The string to be parsed.

  Returns:
    False if the datetime object dosen't exists in the given period else True.
    If string is not parsed returns True.
  """
  period = _PERIOD_REGEX.search(string)
  if period:
    period = period.group(1).lower()
    if period == 'day':
      return True
    elif period == 'weekend':
      return date_time.weekday() in _WEEKEND_DAYS
    elif period == 'weekday':
      return date_time.weekday() not in _WEEKEND_DAYS
    else:
      day_name = date_time.strftime('%a')
      return day_name.lower() == period
  return True


def _ParseDate(date_time, string):
  """Checks whether the datetime object exists in given date range.

  Parses string to get date range and checks whether the datetime object exists
  in parsed date range.

  Args:
    date_time: The datetime object.
    string: The string to be parsed.

  Returns:
    False if the datetime object dosen't exists in the given date range else
    True. If string is not parsed returns True.

  Raises:
    ParseError if string is not parsable.
  """
  date = _DATE_REGEX.search(string)
  available = True
  if date:
    try:
      start_date, end_date = date.group(1), date.group(2)
      if end_date:
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        available = available and end_date.date() >= date_time.date()
      start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
      available = available and start_date <= date_time
      if not end_date:
        available = available and start_date.date() == date_time.date()
    except ValueError:
      raise ParseError('Unable to parse date range. Please user proper format.')
  return available


def _ParseTime(date_time, string):
  """Checks whether the datetime object exists in given time range.

  Parses string to get time range and checks whether the datetime object exists
  in parsed time range.

  Args:
    date_time: The datetime object.
    string: The string to be parsed.

  Returns:
    False if the datetime object dosen't exists in the given time range else
    True. If string is not parsed returns True.

  Raises:
    ParseError if string is not parsable.
  """
  time = _TIME_REGEX.search(string)
  available = True
  if time:
    try:
      start_time, end_time = time.group(1), time.group(2)
      str_date_time = date_time.strftime('%d/%m/%Y ')
      if end_time:
        end_time = datetime.datetime.strptime(
            str_date_time+end_time, '%d/%m/%Y %I:%M %p')
        available = available and end_time >= date_time
      start_time = datetime.datetime.strptime(
          str_date_time+start_time, '%d/%m/%Y %I:%M %p')
      if not end_time:
        available = available and start_time == date_time
      available = available and start_time <= date_time
    except ValueError:
      raise ParseError('Unable to parse time range. Please user proper format.')
  return available


def IsAvailable(date_time, string):
  """Checks whether the datetime object exists in given range.

  Parses string to get a date time range and checks whether the datetime object
  exists in parsed date time range.

  Args:
    date_time: The datetime object.
    string: The string to be parsed.

  Returns:
    False if the datetime object dosen't exists in the given date time range
    else True. If string is not parsed returns True.

  Raises:
    ParseError if string is not parsable.
  """
  return (_ParsePeriod(date_time, string) and
          _ParseDate(date_time, string) and _ParseTime(date_time, string))
