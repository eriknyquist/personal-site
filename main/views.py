import json
import sys
import os
import tempfile

from datetime import datetime

from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import forms
from django.contrib import messages

from .forms import CalendarForm, PTTTLForm

sys.path.insert(0, "generate_life_calendar")
sys.path.insert(0, "ptttl")
sys.path.insert(0, "ptttl/tones")
sys.path.insert(0, "poacher")
sys.path.insert(0, "main")
sys.path.insert(0, '/opt')

import secrets
from repo_monitor import ReposPerMinuteMonitor
from generate_life_calendar import gen_calendar, parse_date
from ptttl_audio_encoder import ptttl_to_mp3, ptttl_to_wav, SINE_WAVE, SQUARE_WAVE

DEFAULT_TITLE = "LIFE CALENDAR"

monitor = ReposPerMinuteMonitor(secrets.GITHUB_UNAME, secrets.GITHUB_PWD)
monitor.start()

def index(request):
    return render(request, 'index.html')

def lastchance(request):
    return render(request, 'lastchance.html')

def music(request):
    return render(request, 'music.html')

def bf(request):
    return render(request, 'bf.html')

def rpm(request):
    data = json.dumps({"repos_per_minute": '%.2f' % monitor.rpm()})
    return HttpResponse(data, content_type='application/json')

def github(request):
    return render(request, 'github.html')

def textgame(request):
    return render(request, 'textgame.html')

def wadenyquist_pdf(request):
    # Read PDF file and create response
    with open('static/docs/wadenyquist.pdf', 'rb') as fh:
        resp = HttpResponse(fh.read(), content_type="application/pdf")
        resp['Content-Disposition'] = ('inline;filename=WadeNyquistPOWPapers.pdf')

    return resp

def wadenyquist(request):
    return render(request, 'wadenyquist.html')

def ptttl(request):
    if request.method == 'POST':
        form = PTTTLForm(request.POST)
        if form.is_valid():
            ptttl_data = form.cleaned_data['ptttl']
            fd, ftemp = tempfile.mkstemp()

            wave = SINE_WAVE if form.cleaned_data['sine'] else SQUARE_WAVE
            if form.cleaned_data['wav']:
                genfunc = ptttl_to_wav
                ext = 'wav'
            else:
                genfunc = ptttl_to_mp3
                ext = 'mp3'

            try:
                genfunc(ptttl_data, ftemp, 0.5, wave)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
                return render(request, 'ptttl.html', {'form': form})

            with open(ftemp, 'rb') as fh:
                mp3_data = fh.read()

            response = HttpResponse(mp3_data, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename=rtttl.%s' % ext
            response['Content-Length'] = os.path.getsize(ftemp)

            os.close(fd)
            os.remove(ftemp)

            return response
    else:
        form = PTTTLForm()

    return render(request, 'ptttl.html', {'form': form})

def get_calendar(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = CalendarForm(request.POST)

        # Fetch form data
        date = form.data['date']
        title = form.data['title']
        filename = tempfile.mktemp()

        try:
            dateobj = parse_date(date)
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return render(request, 'calendar.html', {'form': form})

        dateobj = datetime.combine(dateobj, datetime.min.time())

        # Generate PDF file
        gen_calendar(dateobj, title, filename)

        # Read PDF file and create response
        with open(filename, 'rb') as fh:
            resp = HttpResponse(fh.read(), content_type="application/pdf")
            resp['Content-Disposition'] = ('attachment;filename=my_life_calendar.pdf')

        os.remove(filename)
        render(request, 'calendar.html', {'form': form})
        return resp

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CalendarForm(initial={"title": DEFAULT_TITLE})

    return render(request, 'calendar.html', {'form': form})
