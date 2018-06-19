from django.urls import path

from . import views

urlpatterns = [
    path('calendar/', views.get_calendar, name='get_calendar'),
    path('ptttl/', views.ptttl, name='ptttl'),
]
