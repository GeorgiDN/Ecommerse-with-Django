from django import template
register = template.Library()


@register.filter
def is_favorite(product, user):
    return user.user_favorites.filter(product=product).exists()
