from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lastchance/', views.lastchance, name='lastchance'),
    path('calendar/', views.get_calendar, name='get_calendar'),
    path('github/', views.github, name='github'),
    path('textgame/', views.textgame, name='textgame'),
    path('ptttl/', views.ptttl, name='ptttl'),
    path('wadenyquist/', views.wadenyquist, name='wadenyquist'),
    path('wadenyquist_pdf/', views.wadenyquist_pdf, name='wadenyquist_pdf')
]
