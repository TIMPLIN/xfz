from django import template
from datetime import datetime
from django.utils.timezone import now as now_func, make_aware, localtime


register = template.Library()


@register.filter(name='time_since')
def time_since(value):
    if not isinstance(value, datetime):
        return value

    now = now_func()
    #now = make_aware(datetime.now())
    timestamp = (now - value).total_seconds()

    if timestamp < 60:
        return "刚刚"
    elif 60 <= timestamp < 60 * 60:
        minutes = int(timestamp/60)
        return "%s分钟前"%minutes
    elif 60 * 60 <= timestamp < 60 * 60 * 24:
        hours = int(timestamp/60/60)
        return "%s小时前"%hours
    elif 60 * 60 * 24 <= timestamp <= 60 * 60 * 24 * 30:
        days = int(timestamp/60/60/24)
        return "%s天前"%days
    else:
        return value.strftime('%Y-%m-%d %H:%M')



@register.filter(name='time_format')
def time_format(value):
    if not isinstance(value, datetime):
        return value

    return localtime(value).strftime('%Y-%m-%d %H:%M:%S')