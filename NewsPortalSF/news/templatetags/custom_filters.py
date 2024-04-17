from django import template

register = template.Library()


def censor(value):
    unwanted_words = ['редиска', 'сука', 'блять', 'хуй']
    for word in unwanted_words:
        value = value.replace(word, '*' * len(word))
    return value


register.filter('censor', censor)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
