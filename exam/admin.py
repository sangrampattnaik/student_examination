from django.contrib import admin

# Register your models here.
from .models import Questions, Standard, Student


@admin.register(Standard)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "class_name",
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "standard",
        "date_of_birth",
    ]


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = [
        "question_number",
        "standard",
        "question",
        "option1",
        "option2",
        "option3",
        "option4",
        "correct_answer",
    ]
