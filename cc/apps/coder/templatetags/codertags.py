from django import template

register = template.Library()

@register.inclusion_tag('coder_small.html')
def coder_small(coder, title=None):
	return { 'coder': coder, 'title': title }

@register.inclusion_tag('coder.html')
def coder(coder):
	return { 'coder': coder }