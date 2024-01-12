from django import template
import re


register = template.Library()

@register.filter(name='highlight')
def highlight(value, keyword):
    regex = re.compile(re.escape(keyword), re.IGNORECASE)
    
    def callback(match):
        return f'<span style="color: red; font-weight: bolder;">{ match.group() }</span>'
    
    return regex.sub(callback, value)

@register.filter(name='nameparser')
def nameparser(value):
    namelist = []
    
    for name in value.split(','):
        regex = re.compile(r'\s*and\s*', re.IGNORECASE)
        namelist.append(", ".join([f'<span style="text-decoration-line: underline; cursor: pointer;" onclick="uploadform(this.innerText)">{ name_separate }</span>' for name_separate in regex.split(name) if name_separate is not ""]))
    
    return ", ".join(namelist)
