import datetime


class custom_date():
  def __init__(self, year, month, day):
    self.year = year
    self.month = month
    self.day = day


def date_2_index():
  # date = datetime.datetime.now()
  date = custom_date(2026, 1, 1)
  day_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  return date.year * 365 + sum([day_in_months[m - 1] for m in range(1, date.month)]) + date.day


if __name__ == '__main__':
  print(date_2_index())
