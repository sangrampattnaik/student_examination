from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI
from ninja_api.api import router,GlobalAuth
from ninja_api.api2 import router as student_router
api = NinjaAPI(version="1.0.0",title="Student MCQ Exam API",description="Students for Standard 1 to 10",auth=GlobalAuth())
api.add_router("",router)
api.add_router("",student_router)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]
