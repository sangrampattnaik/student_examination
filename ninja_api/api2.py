from ninja import NinjaAPI, Router, Schema
from ninja.orm import create_schema
from django.http import JsonResponse
from exam.models import Questions, Standard, Student, User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from typing import List

class StudentSchema(Schema):
    username : str
    password : str
    full_name : str
    standard : int

class QuestionSchema(Schema):
    standard : int
    question : str
    option1 : str
    option2 : str
    option3 : str
    option4 : str
    correct_answer:str

class QuestionUpdateSchema(Schema):
    question : str = None
    option1 : str = None
    option2 : str = None
    option3 : str = None
    option4 : str = None
    correct_answer:str = None

class StudentUpdateSchema(Schema):
    full_name : str = None
    standard : int = None

class AnswerSchema(Schema):
    answers:list


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['username','full_name','standard']

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = [
            'id',
            'standard_name',
            'question_number',
            "question",
            "option1",
            "option2",
            "option3",
            "option4",
            'correct_answer'
            ]

class ExamSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = [
            'question_number',
            'id',
            'standard_name',
            "question",
            "option1",
            "option2",
            "option3",
            "option4"
            ]

router = Router()


@router.get("/student",tags=['student'],summary="get list of students")
def student_get(request,standard_id:int=None):
    if standard_id:
        students = Student.objects.filter(standard=standard_id)
    else:
        students = Student.objects.all()
    student_seralizer = StudentSerializer(students,many=True).data
    return JsonResponse({"status":"success","data":student_seralizer},status=200)

@router.post("/student",tags=['student'],summary="create student")
def student_create(request,body:StudentSchema):
    body = body.dict()
    if User.objects.filter(username=body['username']).exists():
        return JsonResponse({"status":"failed","msg":"username already taken"},status=400)
    if (standard := Standard.objects.filter(class_name=body['standard'])).exists():
        user = User.objects.create_user(username=body['username'],password=body['password'])
        std = Student.objects.create(full_name=body['full_name'],standard=standard.first(),user=user)
        std_s = StudentSerializer(std).data
        return JsonResponse({"status":"success","msg":"student created","data":std_s},status=201)
    return JsonResponse({"status":"failed","msg":"standard not found"},status=200)

@router.get("/student/{student_id}",tags=['student'],summary="get particular student")
def student_get_p(request,student_id):
    student = get_object_or_404(Student,id=student_id)
    student_ser = StudentSerializer(student).data
    return JsonResponse({"status":"success","data":student_ser},status=200)

@router.put("/student/{student_id}",tags=['student'],summary="partial and fully update student")
def student_update_p(request,student_id,body:StudentUpdateSchema):
    student = get_object_or_404(Student,id=student_id)
    body = body.dict()
    if body['full_name']:
        student.full_name = body['full_name']
    if body.get('standard'):
        if not int(student.standard.class_name) == body['standard']:
            if (standrd := Standard.objects.filter(class_name = body['standard'])).exists():
                student.standard = standrd.first()
            else:
                return JsonResponse({"status":"failed","msg":"standard not found"},status=404)
    student.save()
    student_ser = StudentSerializer(student).data
    return JsonResponse({"status":"success","msg":"student updated","data":student_ser},status=200)


@router.delete("/student/{student_id}",tags=['student'],summary="delete student")
def student_delete(request,student_id):
    student = get_object_or_404(Student,id=student_id)
    student.delete()
    return JsonResponse({"status":"success","msg":"student deleted"},status=200)

@router.get("/question",tags=['question'],summary="get all question")
def get_questions(request,standard=None):
    '''
    get all questions.
    if standard provided then as per standard, the questions will be displayed
    '''
    if standard:
        qns = Questions.objects.filter(standard=standard)
    else:
        qns = Questions.objects.all()
    q_s = QuestionSerializer(qns,many=True).data
    return JsonResponse({"status":"success","data":q_s},status=200)

@router.post("/question",tags=['question'],summary="create question")
def create_questions(request,body:QuestionSchema):
    body = body.dict()
    if (standard := Standard.objects.filter(class_name__iexact=body['standard'])).exists():
        qns = Questions.objects.create(
            standard=standard.first(),
            correct_answer=body['correct_answer'],
            question=body['question'],
            option1=body['option1'],
            option2=body['option2'],
            option3=body['option3'],
            option4=body['option4']
            )
        q_s = QuestionSerializer(qns).data
        return JsonResponse({"status":"success",'msg':"question created","data":q_s},status=201)
    return JsonResponse({"status":"failed",'msg':"standard not found"},status=404)

@router.get("/question/{question_id}",tags=['question'],summary="get question")
def get_a_qns(request,question_id):
    qns = get_object_or_404(Questions,id=question_id)
    q_s = QuestionSerializer(qns).data
    return JsonResponse({"status":"success","data":q_s},status=200)

@router.put("/question/{question_id}",tags=['question'],summary="partial and fully update a question")
def question_update(request,question_id:int,body:QuestionUpdateSchema):
    qns = get_object_or_404(Questions,id=question_id)
    body = body.dict()
    if body.get('question'):
        qns.question = body['question']
    if body.get('option1'):
        qns.question1 = body['option1']
    if body.get('option2'):
        qns.question2 = body['option2']
    if body.get('option3'):
        qns.question3 = body['option3']
    if body.get('option4'):
        qns.question4 = body['option4']
    if body.get('correct_answer'):
        qns.correct_answer = body['correct_answer']
    qns.save()
    q_s = QuestionSerializer(qns).data
    return JsonResponse({"status":"success","msg":"question updated","data":q_s},status=200)

@router.delete("/question/{question_id}",tags=['question'],summary="delete a question")
def question_delete(request,question_id):
    qns = get_object_or_404(Questions,id=question_id).delete()
    return JsonResponse({"status":"success","msg":"question deleted"},status=200)

@router.get("/exam/{standard}",tags=['test exam'],summary="get all questions by the standard")
def test_exam(request,standard):
    qns = Questions.objects.filter(standard=standard)
    q_s = ExamSerializer(qns,many=True).data
    return JsonResponse({"status":"success","data":q_s},status=200)

@router.post("/exam/{standard}",tags=['test exam'],summary="answers of the questions")
def test_exam(request,standard,body:AnswerSchema):
    body = body.dict()
    answers = body.get('answers')
    questions = Questions.objects.filter(standard=standard)
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
    return JsonResponse(response,status=200)