from django import template
from clothes.models import Edit


def do_edits(parser, token):
    return EditNode()


class EditNode(template.Node):
    def render(self, context):
        context['edits'] = Edit.objects.all().order_by('-created')[:6]
        return ''


register = template.Library()
register.tag('get_edits', do_edits)
