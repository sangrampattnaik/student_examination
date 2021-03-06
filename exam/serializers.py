from rest_framework import serializers
from .models import Questions,Standard,Student

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    standard = StandardSerializer()
    class Meta:
        model = Student
        fields = "__all__"
        fields = "__all__"

class QuestionsSerializer(serializers.ModelSerializer):
    standard = StandardSerializer()
    class Meta:
        model = Questions
        exclude = ['correct_answer']