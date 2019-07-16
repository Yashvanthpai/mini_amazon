from django import template

register = template.Library()
@register.filter(name='modulus')
def xyz(value,arg1):
    return int(value)%int(arg1)

@register.filter(name='length')
def pqr(value):
    return len(value)
    
@register.filter(name='location')
def lmn(value):
    print("/static/product/"+str(value))
    return str("/static/product/"+str(value))
#/static/product/