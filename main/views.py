import json
import sys
import requests
import os
import tempfile
import threading

from datetime import datetime

from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django import forms
from django.contrib import messages

from .forms import CalendarForm, PTTTLForm

sys.path.insert(0, "generate_life_calendar")
sys.path.insert(0, "poacher")
sys.path.insert(0, "main")
sys.path.insert(0, '/opt')
sys.path.insert(0, 'personal-site')

import settings
import secrets
from repo_monitor import ReposPerMinuteMonitor
from generate_life_calendar import gen_calendar, parse_date, parse_darken_until_date
from ptttl.audio import ptttl_to_mp3, ptttl_to_wav
from tones import SINE_WAVE, SQUARE_WAVE

LIFE_CALENDAR_COUNT_KEY = "calendar_downloads"
PTTTL_COUNT_KEY = "ptttl_downloads"
MILLER_HISTORY_COUNT_KEY = "miller_history_downloads"
POW_PAPERS_COUNT_KEY = "pow_papers_downloads"

JSON_FILE = "/home/ubuntu/personal_site_download_counters.json"
DEFAULT_TITLE = "LIFE CALENDAR"

json_file_lock = threading.Lock()
monitor = ReposPerMinuteMonitor(secrets.GITHUB_UNAME, secrets.GITHUB_PWD)
monitor.start()

audio_dir = os.path.join(settings.STATIC_ROOT, "audio")
audio_files = os.listdir(audio_dir)

def read_json_file():
    try:
        with open(JSON_FILE, 'r') as fh:
            attrs = json.load(fh)
    except:
        attrs = {}

    if LIFE_CALENDAR_COUNT_KEY not in attrs:
        attrs[LIFE_CALENDAR_COUNT_KEY] = 0

    if PTTTL_COUNT_KEY not in attrs:
        attrs[PTTTL_COUNT_KEY] = 0

    if MILLER_HISTORY_COUNT_KEY not in attrs:
        attrs[MILLER_HISTORY_COUNT_KEY] = 0

    if POW_PAPERS_COUNT_KEY not in attrs:
        attrs[POW_PAPERS_COUNT_KEY] = 0

    return attrs

def write_json_file(attrs):
    with open(JSON_FILE, 'w') as fh:
        #json.dump({LIFE_CALENDAR_COUNT_KEY: count + 1}, fh)
        json.dump(attrs, fh)

# if a GET (or any other method) we'll create a blank form
def index(request):
    return render(request, 'index.html')

def lastchance(request):
    return render(request, 'lastchance.html')

def music(request):
    return render(request, 'music.html', {"audio_files": audio_files})

def bf(request):
    return render(request, 'bf.html')

def rpm(request):
    data = json.dumps({"repos_per_minute": '%.2f' % monitor.rpm()})
    return HttpResponse(data, content_type='application/json')

def github(request):
    return render(request, 'github.html')

def textgame(request):
    return render(request, 'textgame.html')

def wadenyquist_compressed_pdf(request):
    # Read PDF file and create response
    with json_file_lock: 
        attrs = read_json_file()
        attrs[POW_PAPERS_COUNT_KEY] += 1
        write_json_file(attrs)

    with open('static/docs/wadenyquist_compressed.pdf', 'rb') as fh:
        resp = HttpResponse(fh.read(), content_type="application/pdf")
        resp['Content-Disposition'] = ('inline;filename=WadeNyquistPOWPapers.pdf')

    return resp

def wadenyquist_pdf(request):
    # Read PDF file and create response
    with json_file_lock: 
        attrs = read_json_file()
        attrs[POW_PAPERS_COUNT_KEY] += 1
        write_json_file(attrs)

    with open('static/docs/wadenyquist.pdf', 'rb') as fh:
        resp = HttpResponse(fh.read(), content_type="application/pdf")
        resp['Content-Disposition'] = ('inline;filename=WadeNyquistPOWPapers.pdf')

    return resp

def get_resume(request):
    tex_filename = tempfile.mktemp(dir='.') + '.tex'
    tex_data = requests.get('https://raw.githubusercontent.com/eriknyquist/resume/master/erik_nyquist_cv.tex')

    with open(tex_filename, 'w') as fh:
        fh.write(tex_data.text)

    pdf_filename = tempfile.mktemp(dir='.')
    os.system('pdflatex -jobname=%s %s' % (pdf_filename, tex_filename))

    with open('%s.pdf' % pdf_filename, 'rb') as fh:
        resp = HttpResponse(fh.read(), content_type="application/pdf")
        resp['Content-Disposition'] = ('inline;filename=erik_nyquist_cv.pdf')

    os.remove(tex_filename)
    os.remove(pdf_filename + '.pdf')
    os.remove(pdf_filename + '.aux')
    os.remove(pdf_filename + '.log')
    os.remove(pdf_filename + '.out')

    return resp

def wadenyquist(request):
    return render(request, 'wadenyquist.html')

def deepspacetrader(request):
    return render(request, 'deepspacetrader.html')

def millerfamilyhistory_pdf(request):
    # Read PDF file and create response
    with json_file_lock: 
        attrs = read_json_file()
        attrs[MILLER_HISTORY_COUNT_KEY] += 1
        write_json_file(attrs)

    with open('static/docs/millerfamilyhistory.pdf', 'rb') as fh:
        resp = HttpResponse(fh.read(), content_type="application/pdf")
        resp['Content-Disposition'] = ('inline;filename=MillerFamilyHistory.pdf')

    return resp

def millerfamilyhistory(request):
    return render(request, 'millerfamilyhistory.html')

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

            with json_file_lock: 
                attrs = read_json_file()
                attrs[PTTTL_COUNT_KEY] += 1
                write_json_file(attrs)

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
        age = form.data['age']
        darken = 'darken' in form.data
        filename = tempfile.mktemp()

        try:
            dateobj = parse_date(date)
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return render(request, 'calendar.html', {'form': form})

        dateobj = datetime.combine(dateobj, datetime.min.time())

        if darken:
            darken_date = parse_darken_until_date('today')
        else:
            darken_date = None

        # Generate PDF file
        gen_calendar(dateobj, title, age, filename, darken_date,
                     subtitle_text="Generated for free at https://www.ekn.io/calendar")

        # Read PDF file and create response
        with open(filename, 'rb') as fh:
            resp = HttpResponse(fh.read(), content_type="application/pdf")
            resp['Content-Disposition'] = ('attachment;filename=my_life_calendar.pdf')

        os.remove(filename)
        render(request, 'calendar.html', {'form': form})

        with json_file_lock: 
            attrs = read_json_file()
            attrs[LIFE_CALENDAR_COUNT_KEY] += 1
            write_json_file(attrs)

        return resp

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CalendarForm(initial={"title": DEFAULT_TITLE})

    return render(request, 'calendar.html', {'form': form})
