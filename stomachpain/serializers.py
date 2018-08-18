from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_order_id', 'question_text', 'diagnosis_text', 'recommendations_text', 'contraindications_text', 'precautions_text')
