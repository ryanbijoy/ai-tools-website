from django import template

register = template.Library()

@register.filter
def get_range(value):
    return range(1, value + 1) if value is not None else range(1)

@register.filter
def star_status(value, index):
    if value is None:
        return "bi-star"  # or whatever default you want to use when there are no reviews
    if value >= index:
        return "bi-star-fill"
    elif value >= index - 0.5:
        return "bi-star-half"
    else:
        return "bi-star"
