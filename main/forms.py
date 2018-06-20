from django import forms

DATE_PLACEHOLDER="dd/mm/yyyy"

class CalendarForm(forms.Form):
    title = forms.CharField(label='Calendar title', max_length=30)

    date = forms.DateField(label='Your birthday',
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.TextInput(attrs={'placeholder': DATE_PLACEHOLDER}))
