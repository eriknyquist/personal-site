from django import forms

TITLE_PLACEHOLDER="LIFE CALENDAR"
DATE_PLACEHOLDER="dd/mm/yyyy"

class CalendarForm(forms.Form):
    title = forms.CharField(label='Calendar title', max_length=30,
        widget=forms.TextInput(attrs={'placeholder': TITLE_PLACEHOLDER}))

    date = forms.DateField(label='Your birthday',
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.TextInput(attrs={'placeholder': DATE_PLACEHOLDER}))

    def clean_date(self):
        data = self.cleaned_data['date']
        
        # Remember to always return the cleaned data.
        return data
