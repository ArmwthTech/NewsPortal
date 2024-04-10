from django import template

register = template.Library()


def censor(value):
    unwanted_words = ['редиска', 'сука', 'блять', 'хуй']
    for word in unwanted_words:
        value = value.replace(word, '*' * len(word))
    return value


register.filter('censor', censor)
