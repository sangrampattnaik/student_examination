from django.contrib.auth.models import User
from django.db import models

# Create your models here.
standard_choices = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
]


class Standard(models.Model):
    class_name = models.CharField(max_length=4, choices=standard_choices, unique=True)

    def __str__(self):
        return self.class_name


class Student(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_user')
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40)
    date_of_birth = models.DateField()


class Questions(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField(blank=True, null=True)
    question = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def student_class(self):
        return self.student.standard

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ["question_number"]

    def save(self, *args, **kwargs):
        if not self.question_number:
            self.question_number = Questions.objects.all().count() + 1
        super(Questions, self).save(*args, **kwargs)


# class Score(models.Model):
#     pass
