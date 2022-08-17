from django import template
from clothes.models import Category
from django.db.models import Q

def do_category(parser, token):
    return CategoryNode()


class CategoryNode(template.Node):
    def render(self, context):
        context['categories'] = Category.objects.filter(nav__name='menu')[:6]
        return ''


register = template.Library()
register.tag('get_category', do_category)
