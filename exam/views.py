from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import Questions,QuestionsSerializer,Standard,StandardSerializer,Student,StudentSerializer

class Home(APIView):
    def post(self,request):
        answers = (request.data.get("email"))
        standard = request.data.get("standard")
        questions = Questions.objects.filter(standard=standard)
        print(questions)
        score = 0
        for answer in answers:
            count = questions.filter(correct_answer__iexact=answer[1],id=answer[0]).count()
            if count == 1:
                score += 1
            print(answer[0])
            print(answer[1])
        print(score)
        return Response({"status":"success","score":score})