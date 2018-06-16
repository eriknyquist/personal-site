from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from .forms import CalendarForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CalendarForm(request.POST)
        # check whether it's valid:
        if not form.is_valid():
            messages.error(request, 'Invalid date! please write dd/mm/yyyy or dd-mm-yyyy')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CalendarForm()

    return render(request, 'calendar.html', {'form': form})
