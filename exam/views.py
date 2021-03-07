from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import generics
from .serializers import (
    Questions,
    QuestionsAnswerSerializer,
    QuestionsSerializer,
    Standard,
    StandardSerializer,
    Student,
    StudentSerializer,
    QuestionCreateSerializer
)


class StandardView(ModelViewSet):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer



class StudentRetriveUpdateDestroyAPIView(APIView):
    def get(self,request,student_id):
        try:
            student = Student.objects.get(id=id)
            student_seralizer = StudentSerializer(student)
            return Response({"status":"success","data":student_seralizer.data})
        except Student.DoesNotExist:
            return Response({"status":"success","msg":"student not found"},status=404)
    
    def put(self,request,student_id):
        return Response({"status":"success"})
    
    def delete(self,request,student_id):
        try:
            Student.objects.get(id=student_id).delete()
            return Response({"status":"success","msg":"student deleted"})
        except Student.DoesNotExist:
            return Response({"status":"success","msg":"student not found"},status=404)

class StudentListCreateAPIView(APIView):
    def get(self,request):
        student = Student.objects.all()
        student_seralizer = StudentSerializer(student,many=True)
        return Response({"status":"success","data":student_seralizer.data})

    def post(self,request):
        try:
            body = request.data
            if User.objects.filter(username=body['username']).exists():
                return Response({"status":"failed","msg":"username alreday exist"})
            password = body['password']
            full_name = body['full_name']
            class_name=body['class']
            standard = Standard.objects.get(class_name=class_name)
            user = User.objects.create_user(username=body['username'],password=password)
            student = Student(
                user=user,
                standard=standard,
                full_name=full_name,
            )
            student.save()
            student_serializer = StudentSerializer(student)
            return Response({"status":"success","msg":"student created","data":student_serializer.data},status=201)
        except KeyError as key:
            return Response({"status":"failed","msg":f"{key} required"})
        except Standard.DoesNotExist:
            return Response({"status":"faild","msg":"class does not found"})

class TestExam(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        standards = Standard.objects.filter(class_name=request.user.student_user.standard.class_name).first()
        questions = Questions.objects.filter(standard=standards)
        all_questions = QuestionsSerializer(questions, many=True).data
        return Response({"class": request.user.student_user.standard.class_name, "questions": all_questions})

    def post(self, request):
        answers = request.data.get("answers")
        questions = Questions.objects.filter(standard=request.user.student_user.standard.class_name)
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

class QuestionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Questions.objects.all()
    serializer_class = QuestionCreateSerializer
    
    def get_queryset(self):
        standard = self.request.GET.get("standard")
        if standard:
            return Questions.objects.filter(standard=standard)
        return Questions.objects.all()
        

class QuestionRetriveUpdateDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Questions.objects.all()
    serializer_class = QuestionCreateSerializer
    lookup_field = "id"