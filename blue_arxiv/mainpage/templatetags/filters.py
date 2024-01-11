from django import template
import re


register = template.Library()

@register.filter(name='highlight')
def highlight(value, keyword):
    regex = re.compile(re.escape(keyword), re.IGNORECASE)
    
    def callback(match):
        return f'<span style="color: red; font-weight: bolder;">{ match.group() }</span>'
    
    return regex.sub(callback, value)
