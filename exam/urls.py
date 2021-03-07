from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

routers = DefaultRouter()
routers.register("standard", views.StandardView)

urlpatterns = [
    path("test/", views.TestExam.as_view()),
    path("student/", views.StudentListCreateAPIView.as_view()),
    path("student/<student_id>/", views.StudentRetriveUpdateDestroyAPIView.as_view()),
    path("get-answer/", views.QuestionAnswer.as_view()),
    path("questions/", views.QuestionListCreateAPIView.as_view()),
    path("questions/<id>/", views.QuestionRetriveUpdateDestroyAPIView.as_view()),
    path("", include(routers.urls)),
]
