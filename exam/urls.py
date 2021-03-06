from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from . import views

routers = DefaultRouter()
routers.register("standard", views.StandardView)
routers.register("student", views.StudentView)

urlpatterns = [
    re_path(r"^test/(?P<standard>[0-9]{1,2})$", views.TestExam.as_view()),
    re_path(r"^get-answer/(?P<standard>[0-9]{1,2})$", views.QuestionAnswer.as_view()),
    path("", include(routers.urls)),
]
