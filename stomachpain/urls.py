from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


app_name = 'stomachpain'

urlpatterns = [
    # ex: /stomachpain/
    path('', views.index, name='index'),
    # ex: /stomachpain/edit/id/
    path('edit/<int:question_id>/', views.edit, name='edit'),
    # ex: /stomachpain/delete/id/
    path('delete/<int:question_id>/', views.delete, name='delete'),
    # ex: /stomachpain/add/
    path('add/', views.add, name='add'),
    # ex: /stomachpain/submit/
    path('submit/', views.submit, name='submit'),

    #JSON list of questions
    path('json/list/', views.questions_list_json, name='questions_list_json'),
    #JSON change questions order
    path('json/order/', views.questions_order_update_json, name='questions_order_update_json'),

    # ex: /stomachpain/drug/add
    path('drug/add/', views.drug_add, name='drug_add'),
    # ex: /stomachpain/drug/delete
    path('drug/delete/<int:drug_id>/', views.drug_delete, name='drug_delete'),
    # ex: /stomachpain/drug/add
    path('drug/edit/<int:drug_id>/', views.drug_edit, name='drug_edit'),
    # ex: /stomachpain/drug/submit
    path('drug/submit/', views.drug_submit, name='drug_submit'),

]
