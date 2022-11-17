from datetime import (
    date,
    timedelta,
    datetime,
)
from dateutil.relativedelta import relativedelta
from dateutil.parser import isoparse

from django.utils import timezone


INPUT_FORMATS_DATE = [
    '%m-%Y',
    '%m/%Y',
    '%Y/%m',
    '%Y-%m',
    '%Y-%m-%d',
    '%d-%m-%Y',
    '%Y/%m/%d',
    '%d/%m/%Y',
    '%Y-%m-%d %H:%M:%S',
    '%d-%m-%Y %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%d/%m/%Y %H:%M:%S',
]
DATETIME_OUTPUT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class DateUtils:

    UTC = timezone.utc
    input_format = [
        '%Y-%m',
        '%Y-%m-%d',
        '%m-%Y',
        '%d-%m-%Y',
        '%Y/%m',
        '%Y/%m/%d',
        '%m/%Y',
        '%d/%m/%Y',
    ]

    @staticmethod
    def create(year: int, month: int, day: int):
        return date(year=year, month=month, day=day)

    @staticmethod
    def today() -> date:
        return date.today()

    def today_datetime(self):
        today = datetime.combine(self.today(), datetime.min.time())
        return self.make_aware(today)

    def yesterday_datetime(self):
        return datetime.combine(
            self.today() - timedelta(days=1),
            datetime.min.time(),
        )

    def yesterday(self) -> date:
        return self.now() - timedelta(days=1)

    def tomorrow(self) -> date:
        return self.today() + timedelta(days=1)

    @staticmethod
    def is_naive(datetime_in: datetime) -> bool:
        return datetime_in.tzinfo is None or \
            datetime_in.tzinfo.utcoffset(datetime_in) is None

    @staticmethod
    def is_aware(datetime_in: datetime) -> bool:
        return datetime_in.tzinfo is not None and \
            datetime_in.tzinfo.utcoffset(datetime_in) is not None

    def make_aware(self, datetime_in: datetime) -> datetime:
        """return 2021-06-25 19:27:04 tzinfo=UTC"""
        if self.is_aware(datetime_in):
            return datetime_in.astimezone(self.UTC)

        if self.is_naive(datetime_in):
            return timezone.make_aware(
                datetime_in, self.UTC,
            )
        return self.UTC.localize(datetime_in)

    def make_naive(self, datetime_in: datetime) -> datetime:
        """return 2021-06-25 19:27:04"""
        if self.is_naive(datetime_in):
            return datetime_in
        return timezone.make_naive(
            datetime_in, self.UTC,
        )

    def create_datetime(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> datetime:
        datetime_in = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
        )
        return self.make_aware(datetime_in)

    def create_aware(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> datetime:
        datetime_in = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
        )
        return self.make_aware(datetime_in)

    @staticmethod
    def utcfromtimestamp(unix_time: float) -> datetime:
        return datetime.utcfromtimestamp(unix_time)

    def now(self) -> datetime:
        return timezone.now()

    def cast_from_str(
        self,
        datetime_in: str,
        input_format: str = DATETIME_OUTPUT_FORMAT,
    ) -> datetime:
        datetime_in = datetime.strptime(datetime_in, input_format)
        return self.make_aware(datetime_in)

    def cast_from_datetime(
        self,
        datetime_in: datetime,
        format: str = DATETIME_OUTPUT_FORMAT,
    ) -> str:
        return self.make_naive(datetime_in).strftime(format)

    def cast_from_isoformat(self, datetime_in: str) -> datetime:
        datetime_in = isoparse(datetime_in)
        return self.make_aware(datetime_in)

    def format_str_datetime_str(
        self,
        datetime_in: str,
        input_format: str = DATETIME_OUTPUT_FORMAT,
        output_format: str = DATETIME_OUTPUT_FORMAT,
    ) -> str:
        datetime_in = datetime.strptime(datetime_in, input_format)
        return self.make_aware(datetime_in).strftime(output_format)

    def rest_minutes_to_now(self, minutes=0):
        return self.now() - timedelta(minutes=minutes)

    def rest_days_to_today(self, days_to_rest: int) -> date:
        return self.today() - timedelta(days=days_to_rest)

    def substract_days_from_today(self, days_to_rest: int) -> date:
        return timezone.now() - timedelta(days=days_to_rest)

    def sum_days_to_today(self, days_to_sum: int) -> date:
        return self.today() + timedelta(days=days_to_sum)

    @staticmethod
    def sum_days_to_date(input_date: date, days_to_sum: int) -> date:
        return input_date + timedelta(days=days_to_sum)

    def sum_months_to_today(self, months_to_sum: int) -> date:
        return self.today() + relativedelta(months=months_to_sum)

    def rest_months_to_today(self, months_to_sum: int) -> date:
        return self.today() - relativedelta(months=months_to_sum)

    @staticmethod
    def sum_months_to_date(input_date: date, months_to_sum: int) -> date:
        return input_date + relativedelta(months=months_to_sum)

    @staticmethod
    def rest_months_to_date(input_date: date, months: int) -> date:
        return input_date - relativedelta(months=months)

    @staticmethod
    def rest_days_to_date(input_date: date, days_to_sum: int) -> date:
        return input_date - timedelta(days=days_to_sum)

    @staticmethod
    def get_today_as_str(format='%Y-%m-%d'):
        return date.today().strftime(format)

    @staticmethod
    def get_date_as_str(input_date: date, format='%Y-%m-%d') -> str:
        return input_date.strftime(format)

    @staticmethod
    def get_date_from_str(str_date: str, format='%Y-%m-%d') -> date:
        if not str_date:
            return None
        return datetime.strptime(str_date, format).date()

    @staticmethod
    def diff_month_between_dates(first: date, second: date) -> int:
        return (first.year - second.year) * 12 + first.month - second.month

    @staticmethod
    def diff_days_between_dates(first: date, second: date) -> int:
        return (first - second).days

    def diff_hours_from_now(self, ref_date: datetime):
        return int((self.now() - ref_date).total_seconds() / 60 / 60)

    def replace_day_in_date(self, ref_date: date, from_day: int):
        try:
            valid_date = ref_date.replace(day=from_day)
        except ValueError:
            return self.replace_day_in_date(ref_date, from_day - 1)
        return valid_date

    @staticmethod
    def get_list_datetimes_between_two_datetimes(
        start: datetime,
        end: datetime,
    ) -> list:
        def total_months(dt):
            return dt.month + 12 * dt.year

        mlist = []
        for tot_m in range(total_months(start) - 1, total_months(end)):
            y, m = divmod(tot_m, 12)
            mlist.append(datetime(y, m + 1, 1))
        return mlist

    def date_to_datetime(self, date: date) -> datetime:
        datetime_in = datetime.combine(date, datetime.min.time())
        return self.make_aware(datetime_in)

    def get_future_execution_at_23_or_midnight():
        limit = 23
        future_time = datetime.now()
        test = datetime.now().replace(hour=limit, minute=0, second=0)
        if future_time < test:
            future_time = future_time.replace(hour=limit)
        else:
            future_time = future_time + timedelta(hours=1)
        return future_time

    def get_monday_morning_this_week():
        monday = datetime.now()
        monday = monday - timedelta(days=monday.weekday())
        monday = monday.replace(hour=6)
        return monday
