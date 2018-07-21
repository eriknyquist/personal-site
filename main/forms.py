from django import forms
from django.forms import ValidationError

DATE_PLACEHOLDER = "dd/mm/yyyy"
PTTTL_PLACEHOLDER = "Paste RTTTL/PTTTL code here..."

class PTTTLForm(forms.Form):
    ptttl = forms.CharField(widget=forms.Textarea(attrs={'class': 'multiline_input',
        'placeholder': PTTTL_PLACEHOLDER, 'id': 'ptttl'}))

    sine = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(attrs={'id':'sine', 'onclick':
        "exclusiveClick(this, 'square')"}))
    square = forms.BooleanField(required=False, initial=True,
        widget=forms.CheckboxInput(attrs={'id':'square', 'onclick':
        "exclusiveClick(this, 'sine')"}))

    wav = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(attrs={'id':'wav', 'onclick':
        "exclusiveClick(this, 'mp3')"}))
    mp3 = forms.BooleanField(required=False, initial=True,
        widget=forms.CheckboxInput(attrs={'id':'mp3', 'onclick':
        "exclusiveClick(this, 'wav')"}))

class CalendarForm(forms.Form):
    title = forms.CharField(label='Calendar title', max_length=30)

    date = forms.DateField(label='Your birthday',
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.TextInput(attrs={'placeholder': DATE_PLACEHOLDER}))
