from django import forms
from .models import Drug
from .validators import validate_file_extension

class QuestionForm(forms.Form):
	question_id = forms.CharField(label='',widget=forms.HiddenInput())
	question_order_id = forms.CharField(widget=forms.HiddenInput())
	question_text = forms.CharField(label='Вопрос:', required=False)
	diagnosis_text = forms.CharField(label='Диагноз:', widget=forms.Textarea, required=False)
	recommendations_text = forms.CharField(label='Рекомендации:', widget=forms.Textarea, required=False)
	interrupt_boolean = forms.BooleanField(label='Прервать опросник в связи с состоянием пациента', required=False)
	drugs = forms.ModelMultipleChoiceField(label='Рекомендуемые препараты', required=False, widget=forms.CheckboxSelectMultiple, queryset=Drug.objects.all())

class DrugForm(forms.Form):
	drug_id = forms.CharField(label='',widget=forms.HiddenInput())
	drug_name = forms.CharField(label='Название препарата:')
	image_file = forms.ImageField(label='Изображение:', required=False, validators=[validate_file_extension], widget=forms.ClearableFileInput)
	contraindications_text = forms.CharField(label='Противопоказания:', widget=forms.Textarea, required=False)
	precautions_text = forms.CharField(label='Предосторожности:', widget=forms.Textarea, required=False)
	drug_guide_url = forms.URLField(label='Ссылка на препарат:', required=False)




