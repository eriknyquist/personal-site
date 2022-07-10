from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lastchance/', views.lastchance, name='lastchance'),
    path('calendar/', views.get_calendar, name='get_calendar'),
    path('github/', views.github, name='github'),
    path('bf/', views.bf, name='bf'),
    path('rpm/', views.rpm, name='rpm'),
    path('textgame/', views.textgame, name='textgame'),
    path('ptttl/', views.ptttl, name='ptttl'),
    path('music/', views.music, name='music'),
    path('wadenyquist/', views.wadenyquist, name='wadenyquist'),
    path('deepspacetrader/', views.deepspacetrader, name='deepspacetrader'),
    path('wadenyquist_pdf/', views.wadenyquist_pdf, name='wadenyquist_pdf'),
    path('wadenyquist_compressed_pdf/', views.wadenyquist_compressed_pdf, name='wadenyquist_compressed_pdf'),
    path('millerfamilyhistory/', views.millerfamilyhistory, name='millerfamilyhistory'),
    path('millerfamilyhistory_pdf/', views.millerfamilyhistory_pdf, name='millerfamilyhistory_pdf'),
    url(r'^favicon.ico$',
        RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')),
        name="favicon")
]
