from django import template
from clothes.models import Type
from django.db.models import Q


def do_type(parser, token):
    return TypeNode()


class TypeNode(template.Node):
    def render(self, context):
        context['types'] = Type.objects.all()
        return ''


register = template.Library()
register.tag('get_type', do_type)
