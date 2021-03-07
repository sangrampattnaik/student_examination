from rest_framework import serializers

from .models import Questions, Standard, Student,User


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = "__all__"
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = "__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        exclude = ["correct_answer", "standard"]


class QuestionsAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        exclude = ["standard"]

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"