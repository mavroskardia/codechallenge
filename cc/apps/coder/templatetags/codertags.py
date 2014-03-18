from django import template

register = template.Library()

@register.inclusion_tag('coder.html')
def coder(coder):
	return { 'coder': coder }