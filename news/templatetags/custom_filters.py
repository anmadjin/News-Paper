from django import template
from django.template.defaultfilters import stringfilter
from ..resource import BUN_WORDS

register = template.Library()

@register.filter
@stringfilter
def censor(value):
    res = value
    for word in BUN_WORDS:
        variants = [
            word,
            word.capitalize(),
            word.upper(),
        ]

        for var in variants:
            if var in res:
                censored = var[0] + '*' * (len(var) - 1)
                res = res.replace(var, censored)

    return res