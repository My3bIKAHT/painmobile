from django.urls import path
from . import views


app_name = 'pain'

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
]



