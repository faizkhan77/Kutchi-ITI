from django import template
from datetime import timedelta

register = template.Library()


# using this so i will be able to add 1 day to the completion date of course to give the exam date
@register.filter(name="add_days")
def add_days(value, days):
    return value + timedelta(days=days)


# to substract amount_paid from coursefees field
@register.filter
def subtract(value, arg):
    return value - arg
