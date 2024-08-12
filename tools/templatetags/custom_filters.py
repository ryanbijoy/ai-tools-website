from django import template

register = template.Library()


@register.filter
def get_range(value):
    try:
        return range(1, int(value) + 1) if value is not None else range(1)
    except (ValueError, TypeError):
        return range(1)


@register.filter
def star_status(value, index):
    try:
        value = float(value)
        index = int(index)
    except (ValueError, TypeError):
        return "bi-star"

    if value is None:
        return "bi-star"
    if value >= index:
        return "bi-star-fill"
    elif value >= index - 0.5:
        return "bi-star-half"
    else:
        return "bi-star"
