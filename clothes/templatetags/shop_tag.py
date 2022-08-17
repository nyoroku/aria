from django import template
from clothes.models import Shop


def do_shops(parser, token):
    return ShopNode()


class ShopNode(template.Node):
    def render(self, context):
        context['shops'] = Shop.objects.all().order_by('-created')[:6]
        return ''


register = template.Library()
register.tag('get_shops', do_shops)
