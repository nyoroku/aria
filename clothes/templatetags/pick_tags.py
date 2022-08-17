from django import template
from clothes.models import Product
from django.db.models import Q

def do_picks(parser, token):
    return PickNode()


class PickNode(template.Node):
    def render(self, context):
        context['picks'] = Product.objects.filter(pick=True)[:6]
        return ''


register = template.Library()
register.tag('get_picks', do_picks)
