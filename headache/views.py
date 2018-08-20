from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Max
from django import forms


# Create your views here.

from .models import Question, Drug
from .forms import QuestionForm, DrugForm

# Imports for REST API

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import QuestionSerializer

from .dictionary import dictionary

# file upload functions

from .file_management import handle_uploaded_file

def index(request):
    latest_question_list = Question.objects.order_by('question_order_id')
    latest_drug_list = Drug.objects.order_by('id')
    context = {
    	'latest_question_list': latest_question_list,
    	'latest_drug_list': latest_drug_list,
    	'dictionary': dictionary,
    }
    return render(request, 'headache/index.html', context)

def edit(request, question_id):
	# если question_id не указан, то будет вызвана ошибка 404
	question_to_edit = get_object_or_404(Question, pk=question_id)
	# Заполняем форму данными из БД
	form = QuestionForm( initial= {
		'question_id': question_to_edit.id,
		'question_order_id': question_to_edit.question_order_id,
		'question_text': question_to_edit.question_text,
		'diagnosis_text': question_to_edit.diagnosis_text,
		'recommendations_text': question_to_edit.recommendations_text,
		'interrupt_boolean': question_to_edit.interrupt_boolean,
		'drugs': question_to_edit.drugs.all(),
		})
	message = 'Редактировать вопрос'
	return render(request, 'headache/question.html', {'form': form, 'message': message, 'dictionary': dictionary,})

def delete(request, question_id):
	if question_id>0:
		question_to_delete = get_object_or_404(Question, pk=question_id)
		question_to_delete.delete()
		# После удаления записи сортируем вопросы по заданному порядку
		# и выводим index
		return redirect('/headache/')
	else: 
		raise forms.ValidationError("Не указан или неверный номер для удаления")

def add(request):
	# выводим пустую форму
	# --------------------
	# получаем максимальный порядковый номер в списке вопросов
	# и делаем инкремент
	tmp = Question.objects.all().aggregate(Max('question_order_id'))['question_order_id__max']
	if tmp is None:
		max_question_order_id = 0
	else:
		max_question_order_id = int(tmp)
	form = QuestionForm( initial= {
		'question_order_id': max_question_order_id+1,
		'question_id': -1,
		})
	message = 'Добавить вопрос'
	return render(request, 'headache/question.html', {'form': form, 'message': message, 'dictionary': dictionary,})

def submit(request):
	# Возможны два случая submit:
 	# - В submit передаются данные нового вопроса [add] => question_id = -1
	# - В submit передаются данные редактируемого вопроса [edit], question_id = текущему id autoincrement вопроса
	#
	# Проверяем чтобы данные были переданы через POST
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			# Проверяем новая ли это запись или редактируемая
			if form.cleaned_data['question_id'] == "-1":
				# case: новая
				# создаем новый объект Question
				question_to_add = Question()
				# заполняем его
				tmp = Question.objects.all().aggregate(Max('question_order_id'))['question_order_id__max']
				if tmp is None:
					max_question_order_id = 1
				else:
					max_question_order_id = int(tmp)+1
				question_to_add.question_order_id = max_question_order_id
				question_to_add.question_text = form.cleaned_data['question_text']
				question_to_add.diagnosis_text = form.cleaned_data['diagnosis_text']
				question_to_add.recommendations_text = form.cleaned_data['recommendations_text']
				question_to_add.interrupt_boolean = form.cleaned_data['interrupt_boolean']
				question_to_add.save()
				drugs_list = form.cleaned_data['drugs']
				drugs_list_ids = [drugs_list.id for drugs_list in drugs_list]
				drugs = Drug.objects.filter(id__in=drugs_list_ids)
				for drug in drugs:
					question_to_add.drugs.add(drug)
				question_to_add.save()
				# выводим редактор с заполненными полями
				#return render(request, 'headache/question.html', {'form': form, 'dictionary': dictionary,})
				return redirect('/headache/')
			else:
				#case: редактируем
				# вытаскиваем из БД объект с нужным id
				question_to_edit = get_object_or_404(Question, pk=form.cleaned_data['question_id'])
				# переписываем поля
				question_to_edit.question_order_id = form.cleaned_data['question_order_id']
				question_to_edit.question_text = form.cleaned_data['question_text']
				question_to_edit.diagnosis_text = form.cleaned_data['diagnosis_text']
				question_to_edit.recommendations_text = form.cleaned_data['recommendations_text']
				question_to_edit.interrupt_boolean = form.cleaned_data['interrupt_boolean']
				# выгружаем список drugs
				drugs_list = form.cleaned_data['drugs']
				drugs_list_ids = [drugs_list.id for drugs_list in drugs_list]
				drugs = Drug.objects.filter(id__in=drugs_list_ids)
				question_to_edit.drugs.clear()
				for drug in drugs:
					question_to_edit.drugs.add(drug)
				question_to_edit.save()
				# выводим редактор с заполненными полями
				# return render(request, 'headache/question.html', {'form': form, 'dictionary': dictionary,})
				return redirect('/headache/')
		else:
			raise forms.ValidationError("Неверные данные в форме")
	else:
		raise forms.ValidationError("Неверный метод передачи данных (не POST) или данные отсутствуют")

@csrf_exempt
def questions_list_json(request):
    ###############
    # List all questions
    ###############
	questions = Question.objects.all().order_by('question_order_id')
	serializer = QuestionSerializer(questions, many = True)
	return JsonResponse(serializer.data, safe = False)

@csrf_exempt
def questions_order_update_json(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		print(data)
		for record in data:
			question_id = int(record['question_id'])
			question_to_order = get_object_or_404(Question, pk=question_id)
			question_to_order.question_order_id = int(record['order_id'])
			question_to_order.save()
		return HttpResponse( content_type = "application/json",status = 200)
	else:
		return JsonResponse(serializer.errors, status = 400)

def drug_add(request):
	# выводим пустую форму для добавления препарата
	form = DrugForm( initial= {
		'drug_id': -1,
		})
	message = 'Добавить препарат'
	return render(request, 'headache/drug.html', {'form': form, 'message': message, 'dictionary': dictionary,})

def drug_edit(request, drug_id):
	# если drug_id не указан, то будет вызвана ошибка 404
	drug_to_edit = get_object_or_404(Drug, pk=drug_id)
	# Заполняем форму данными из БД
	form = DrugForm( initial= {
		'drug_id': drug_to_edit.id,
		'image_file': drug_to_edit.image_file,
		'drug_name': drug_to_edit.drug_name,
		'contraindications_text': drug_to_edit.contraindications_text,
		'precautions_text': drug_to_edit.precautions_text,
		'drug_guide_url': drug_to_edit.drug_guide_url,
		})
	message = 'Редактировать препарат'
	if drug_to_edit.image_file:
		image_url = drug_to_edit.image_file.url
	else:
		image_url = None
	return render(request, 'headache/drug.html', {'form': form, 'message': message, 'drug_id': drug_id, 'image_url': image_url, 'dictionary': dictionary, })


def drug_delete(request, drug_id):
		drug_to_delete = get_object_or_404(Drug, pk=drug_id)
		drug_to_delete.delete()
		return redirect('/headache/')

def drug_submit(request):
	# Возможны два случая submit:
 	# - В submit передаются данные нового препарата [add] => drug_id = -1
	# - В submit передаются данные редактируемого препарата [edit], drug_id = текущему id = primary_key
	#
	# Проверяем чтобы данные были переданы через POST
	if request.method == 'POST':
		form = DrugForm(request.POST, request.FILES)
		if form.is_valid():
			# Проверяем новая ли это запись или редактируемая
			if form.cleaned_data['drug_id'] == "-1":
				# case: новая
				# создаем новый объект Drug
				drug_to_add = Drug()
				# заполняем Drug
				drug_to_add.drug_name = form.cleaned_data['drug_name']
				drug_to_add.contraindications_text = form.cleaned_data['contraindications_text']
				drug_to_add.precautions_text = form.cleaned_data['precautions_text']
				drug_to_add.drug_guide_url = form.cleaned_data['drug_guide_url']
				# сохраняем изображение
				if 'image_file' in request.FILES:
					drug_to_add.image_file = request.FILES['image_file']
				else:
					drug_to_add.image_file = None
				drug_to_add.save()
				return redirect('/headache/')
			else:
				#case: редактируем
				# вытаскиваем из БД объект с нужным id
				drug_to_edit = get_object_or_404(Drug, pk=form.cleaned_data['drug_id'])
				# переписываем поля
				drug_to_edit.drug_name = form.cleaned_data['drug_name']
				drug_to_edit.contraindications_text = form.cleaned_data['contraindications_text']
				drug_to_edit.precautions_text = form.cleaned_data['precautions_text']
				drug_to_edit.drug_guide_url = form.cleaned_data['drug_guide_url']

				# четыре случая: 
				# - картинка не приложена, галочка на удаление не стоит
				# - картинка приложена, галочка на удаление не стоит
				# - картинка не приложена, галочка стоит
				# - картинка приложена, галочка стоит

				if 'image_file-clear' in request.POST:
					# если стоит галочка "удалить картинку"
					drug_to_edit.image_file = None
				else:
					if 'image_file' in request.FILES:
						# если файл приложили
						drug_to_edit.image_file = request.FILES['image_file']
						# если файл не приложили
						# НИЧЕГО НЕ ДЕЛАЕМ
				drug_to_edit.save()
				return redirect('/headache/')
				
		else:
			raise forms.ValidationError(form.errors)
	else:
		raise forms.ValidationError("Неверный метод передачи данных (не POST) или данные отсутствуют")

