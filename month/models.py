from django.db import models
from month import forms
from month import widgets
from month import Month
import datetime


# Patch python3 basestring
# Credits @leingang
# https://github.com/oxplot/fysom/issues/1

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

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
        #defaults = {'widget': self.widget}
        #defaults.update(kwargs)
        #return forms.MonthField(**defaults)

        #The widget is allready being specified somewhere by models.DateField...
        kwargs['widget'] = self.widget
        return forms.MonthField(**kwargs)
