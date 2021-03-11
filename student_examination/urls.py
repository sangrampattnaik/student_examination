from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI
from ninja_api.api import router
from ninja_api.api2 import router as student_router
api = NinjaAPI()
api.add_router("",router)
api.add_router("",student_router)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]
