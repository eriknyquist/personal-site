import sys
import os

from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import forms

from .forms import CalendarForm

sys.path.insert(0, "generate_life_calendar")

from generate_life_calendar import gen_calendar

DEFAULT_TITLE = "LIFE CALENDAR"

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = CalendarForm(request.POST)

        # check whether it's valid
        if form.is_valid():
            # Fetch form data
            date = form.cleaned_data['date']
            title = form.cleaned_data['title']
            filename = 'my_life_calendar.pdf'
            dateobj = datetime.combine(date, datetime.min.time())

            # Generate PDF file
            gen_calendar(dateobj, title, filename)

            # Read PDF file and create response
            with open(filename, 'rb') as fh:
                resp = HttpResponse(fh.read(), content_type="application/pdf")
                resp['Content-Disposition'] = ('attachment;filename='
                    + os.path.basename(filename))

            return resp
        else:
            messages.error(request,
                'Invalid date! please write dd/mm/yyyy or dd-mm-yyyy')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CalendarForm(initial={"title": DEFAULT_TITLE})

    return render(request, 'calendar.html', {'form': form})
