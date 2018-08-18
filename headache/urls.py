from django.urls import path


from . import views


app_name = 'headache'

urlpatterns = [
    # ex: /headache/
    path('', views.index, name='index'),
    # ex: /headache/edit/id/
    path('edit/<int:question_id>/', views.edit, name='edit'),
    # ex: /headache/delete/id/
    path('delete/<int:question_id>/', views.delete, name='delete'),
    # ex: /headache/add/
    path('add/', views.add, name='add'),
    # ex: /headache/submit/
    path('submit/', views.submit, name='submit'),

    #JSON list of questions
    path('json/list/', views.questions_list_json, name='questions_list_json'),
    #JSON change questions order
    path('json/order/', views.questions_order_update_json, name='questions_order_update_json'),

    # ex: /headache/drug/add
    path('drug/add/', views.drug_add, name='drug_add'),
    # ex: /headache/drug/delete
    path('drug/delete/<int:drug_id>/', views.drug_delete, name='drug_delete'),
    # ex: /headache/drug/add
    path('drug/edit/<int:drug_id>/', views.drug_edit, name='drug_edit'),
    # ex: /headache/drug/submit
    path('drug/submit/', views.drug_submit, name='drug_submit'),

]



