import re
import types

from django import template
from django.template import Node, TemplateSyntaxError
from django.template.loader import render_to_string

register = template.Library()


def silence_without_field(f):
    def wrapped(field, attr):
        if not field:
            return ""
        return f(field, attr)

    return wrapped


@register.filter("attr")
@silence_without_field
def set_attr(field, attr):
    def process(widget, attrs, attribute, value):
        attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter(name='field_type')
def field_type(field):
    """
    Template filter that returns field class name (in lower case).
    E.g. if field is CharField then {{ field|field_type }} will
    return 'charfield'.
    """
    if hasattr(field, 'field') and field.field:
        return field.field.__class__.__name__.lower()
    return ''


@register.filter(name='widget_type')
def widget_type(field):
    """
    Template filter that returns field widget class name (in lower case).
    E.g. if field's widget is TextInput then {{ field|widget_type }} will
    return 'textinput'.
    """
    if hasattr(field, 'field') and hasattr(field.field, 'widget') and field.field.widget:
        return field.field.widget.__class__.__name__.lower()
    return ''


# ======================== field_tag tag ==============================
#
ATTRIBUTE_RE = re.compile(r"""(?P<attr>[\w_-]+)(?P<sign>\+?=)(?P<value>['"]? # start quote
        [^"']*['"]? # end quote
    )""", re.VERBOSE | re.UNICODE)


@register.tag
def field_tag(parser, token):
    """
    Render a form field using given attribute-value pairs
    Takes form field as first argument and list of attribute-value pairs for
    all other arguments.  Attribute-value pairs should be in the form of
    attribute=value or attribute="a value" for assignment and attribute+=value
    or attribute+="value" for appending.
    """
    error_msg = '%r tag requires a form field followed by a list of attributes and values in ' \
                'the form attr="value"' % \
                token.split_contents()[0]
    try:
        bits = token.split_contents()
        form_field = bits[1]
        attr_list = bits[2:]
    except ValueError:
        raise TemplateSyntaxError(error_msg)

    form_field = parser.compile_filter(form_field)

    set_attrs = []
    append_attrs = []
    for pair in attr_list:
        match = ATTRIBUTE_RE.match(pair)
        if not match:
            raise TemplateSyntaxError(error_msg + ": %s" % pair)
        dct = match.groupdict()
        attr, sign, value = dct['attr'], dct['sign'], parser.compile_filter(dct['value'])

        if sign == "=":
            set_attrs.append((attr, value))
        else:
            append_attrs.append((attr, value))
    return FieldAttributeNode(form_field, set_attrs, append_attrs)


class FieldAttributeNode(Node):
    def __init__(self, field, set_attrs, append_attrs):
        self.field = field
        self.set_attrs = set_attrs
        self.append_attrs = append_attrs

    def render(self, context):
        bounded_field = self.field.resolve(context)
        field = getattr(bounded_field, 'field', None)
        if getattr(bounded_field, 'errors', None) and 'WIDGET_ERROR_CLASS' in context:
            bounded_field = append_attr(bounded_field, 'class:%s' %
                                        context['WIDGET_ERROR_CLASS'])
        if field and field.required and 'WIDGET_REQUIRED_CLASS' in context:
            bounded_field = append_attr(bounded_field, 'class:%s' %
                                        context['WIDGET_REQUIRED_CLASS'])
        bounded_field.label = ""
        for k, v in self.set_attrs:
            if k == 'label':
                bounded_field.label = v.resolve(context)
            elif k == 'err_class':
                bounded_field.err_class = v.resolve(context)
            elif k == 'type':
                bounded_field.field.widget.input_type = v.resolve(context)
            else:
                bounded_field = set_attr(bounded_field, '%s:%s' % (k, v.resolve(context)))
        for k, v in self.append_attrs:
            bounded_field = append_attr(bounded_field, '%s:%s' % (k, v.resolve(context)))
        return render_to_string('farjad/_field_handler.html', context={'field': bounded_field})


@register.filter
def max_objects_count(objects_list, num):
    if len(objects_list) > num:
        return objects_list[:num]
    return objects_list


@register.filter("append_attr")
@silence_without_field
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


def _process_field_attributes(field, attr, process):
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field
