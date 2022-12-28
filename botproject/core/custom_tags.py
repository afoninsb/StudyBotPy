from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    """Получаем значение словаря по его ключу."""
    return dictionary.get(key)
