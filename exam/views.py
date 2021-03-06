from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import (
    Questions,
    QuestionsAnswerSerializer,
    QuestionsSerializer,
    Standard,
    StandardSerializer,
    Student,
    StudentSerializer,
)


class StandardView(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer


class StudentView(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TestExam(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        standards = Standard.objects.filter(class_name=request.user.student_user.class_name).first()
        questions = Questions.objects.filter(standard=standards)
        all_questions = QuestionsSerializer(questions, many=True).data
        return Response({"class": request.user.student_user.class_name, "questions": all_questions})

    def post(self, request):
        answers = request.data.get("answers")
        questions = Questions.objects.filter(standard=request.user.student_user.class_name)
        total_questions = questions.count()
        question_attempt = 0
        wright_answer = 0
        wrong_answer = 0
        score = 0
        if answers:
            for answer in answers:
                try:
                    correct_answer_count = questions.filter(
                        correct_answer__iexact=answer[1], id=answer[0]
                    ).count()
                    question_attempt += 1
                    if correct_answer_count == 1:
                        score += 4
                        wright_answer += 1
                    elif correct_answer_count == 0:
                        score -= 0.25
                        wrong_answer += 1
                except IndexError:
                    pass
            response = {
                "total_questions": total_questions,
                "question_attempt": question_attempt,
                "wright_answer": wright_answer,
                "wrong_answer": wrong_answer,
                "score": score,
            }
        else:
            response = {
                "total_questions": total_questions,
                "question_attempt": 0,
                "wright_answer": 0,
                "wrong_answer": 0,
                "score": 0,
            }
        return Response(response)


class QuestionAnswer(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        standards = Standard.objects.filter(class_name=request.user.student_user.class_name).first()
        questions = Questions.objects.filter(standard=standards)
        all_questions = QuestionsAnswerSerializer(questions, many=True).data
        return Response({"class": request.user.student_user.class_name, "questions": all_questions})
