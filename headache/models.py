from django.db import models
from django.conf import settings
# Create your models here.

class Drug(models.Model):
    drug_name = models.CharField('Название препарата', max_length=200, default="")
    image_file = models.ImageField(null=True, blank=True)
    contraindications_text = models.CharField('Есть ли у вас (противопоказания)', max_length=2000, default="")
    precautions_text = models.CharField('Есть ли у вас (предостережения)', max_length=2000, default="")
    drug_guide_url = models.URLField('Ссылка на препарат')
    def __str__(self):
        return self.drug_name

class Question(models.Model):
    question_order_id = models.IntegerField('Порядковый номер', default=0)
    question_text = models.CharField('Текст вопроса', max_length=100, default="")
    diagnosis_text = models.CharField('Диагноз', max_length=2000, default="")
    recommendations_text = models.CharField('Рекомендации', max_length=2000, default="")
    interrupt_boolean = models.BooleanField(default=False)
    drugs = models.ManyToManyField(Drug)

    def __str__(self):
        return self.question_text

