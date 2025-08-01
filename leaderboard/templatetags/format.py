from datetime import datetime

from django import template

register = template.Library()

@register.filter(name="format_score")
def format_score(value: datetime)-> str:
    if value:
        return f"{str(value.hour + (value.day - 1) * 24)+':' if value.hour else ''}{('0' if value.minute < 10 else '') + str(value.minute)}:{('0' if value.second < 10 else '') + str(value.second)}{','+('0'*(3-len(str(value.microsecond//1000))) + str(value.microsecond//1000))}"
    else:
        return "null"