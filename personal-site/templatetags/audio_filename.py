#audio_filename.py
import os
from django import template
 
register = template.Library()

@register.filter
def audio_filename(value):
    return os.path.splitext(os.path.basename(value))[0]
