from django.db import models
import datetime
from month import forms
from month import widgets

def days(days):
    return datetime.timedelta(days=days)

class Month(object):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self._date = datetime.date(year=self.year, month=self.month, day=1)

    @classmethod
    def from_int(cls, months):
        y, m = divmod(months, 12)
        m += 1
        return cls(y, m)

    @classmethod
    def from_date(cls, date):
        return cls(date.year, date.month)
    
    @classmethod
    def from_string(cls, date):
        y = int(date[:4])
        m = int(date[5:7])
        return cls(y, m)
    def __add__(self, months):
        return Month.from_int(int(self) + months)
    def next_month(self):
        return self + 1
    def prev_month(self):
        return self + (-1)
    def first_day(self):
        return self._date
    def last_day(self):
        return self.next_month().first_day() - days(1)
    def __int__(self):
        return self.year * 12 + self.month - 1
    def __contains__(self, date):
        return self == date
    def __eq__(self, x):
        if isinstance(x, Month):
            return x.month == self.month and x.year == self.year
        if isinstance(x, datetime.date):
            return self.year == x.year and self.month == x.month
        if isinstance(x, int):
            return x == int(self)
        if isinstance(x, basestring):
            return str(self) == x[:7]
    def __gt__(self, x):
        if isinstance(x, Month):
            if self.year != x.year: return self.year > x.year
            return self.month > x.month
        if isinstance(x, datetime.date):
            return self.first_day() > x
        if isinstance(x, int):
            return int(self) > x
        if isinstance(x, basestring):
            return str(self) > x[:7]
    def __ne__(self, x):
        return not self == x
    def __le__(self, x):
        return not self > x
    def __ge__(self, x):
        return (self > x) or (self == x)
    def __lt__(self, x):
        return not self >= x
    def __str__(self):
        return '%s-%02d' %(self.year, self.month)
    def __unicode__(self):
        return self.__str__()
    def __repr__(self):
        return self.__str__()
    def datestring(self):
        return self.first_day().isoformat()


class MonthField(models.DateField):
    description = "A specific month of a specific year."
    widget = widgets.MonthSelectorWidget
    def to_python(self, value):
        if isinstance(value, Month):
            month = value
        elif isinstance(value, datetime.date):
            month = Month.from_date(value)
        elif isinstance(value, basestring):
            month = Month.from_string(value)
        else:
            month = None
        return month

    def get_prep_value(self, value):
        month = self.to_python(value)
        if month is not None:
            return month.first_day()
        return None
        
    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def clean(self, value, instance):
        return self.to_python(value)

    def formfield(self, **kwargs):
        del(kwargs['widget'])#This is a hack and I'm not sure why it is necessary.
        return forms.MonthField(**kwargs)

class Example(models.Model):
    name = models.CharField(max_length=20, blank=True)
    month = MonthField()
    def __unicode__(self):
        return unicode(self.month)