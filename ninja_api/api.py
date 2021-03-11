from ninja import NinjaAPI, Router, Schema
from ninja.orm import create_schema
from django.http import JsonResponse
from exam.models import Questions, Standard, Student, User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from django.conf import settings
import jwt
from ninja.security import HttpBearer
class GlobalAuth(HttpBearer):
    openapi_scheme = "sdfnvl"
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
            print(payload)
            return payload
        except jwt.exceptions.DecodeError:
            raise AuthorizationFailed("authorization failed")
        except jwt.exceptions.InvalidSignatureError:
            raise AuthorizationFailed("authorization failed")
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthorizationFailed("token has been expired")
        except Person.DoesNotExist:
            raise AuthorizationFailed("authorization failed.no data found")
        except jwt.exceptions.InvalidTokenError:
            raise AuthorizationFailed("authorization failed")

class StandardSchema(Schema):
    class_name:str

class LoginSchema(Schema):
    username:str
    password:str

class StandardSerializer(ModelSerializer):
    class Meta:
        model = Standard
        fields = "__all__"

router = Router()

@router.get("/standard",tags=['standard'],summary="get list of standards")
def standard_get(request):
    print(request.auth)
    standards = Standard.objects.all()
    standards_serilaizer = StandardSerializer(standards,many=True).data
    return JsonResponse({"status":"success","data":standards_serilaizer},status=200)

@router.post("/standard",tags=['standard'],summary="create standard")
def standard_create(request,body:StandardSchema):
    body = body.dict()
    print(body)
    if Standard.objects.filter(class_name__iexact=body['class_name']).exists():
        return JsonResponse({"status":"failed",'msg':"standard already exist"},status=400)
    std = Standard.objects.create(class_name=body['class_name'])
    std_ser = StandardSerializer(std).data
    return JsonResponse({"status":"success",'msg':"stanard created","data":std_ser},status=201)


@router.get("/standard/{standard_id}",tags=['standard'],summary="get particular standard")
def standard_get_particular(request,standard_id):
    try:
        std = Standard.objects.get(id=standard_id)
        std_ser = StandardSerializer(std).data
        return JsonResponse({"status":"success","data":std_ser},status=201)
    except Standard.DoesNotExist:
        return JsonResponse({"status":"failed",'msg':"details not found"},status=404)

@router.put("/standard/{standard_id}",tags=['standard'],summary="partial and fully update a standard")
def standard_update_particular(request,standard_id,body:StandardSchema):
    std = get_object_or_404(Standard,id=standard_id)
    body = body.dict()
    if body['class_name'] == std.class_name:
        pass
    else:
        if Standard.objects.filter(class_name__iexact=body['class_name']).exists():
            return {"status":"failed"}
        std.class_name = body['class_name']
        std.save()
    return {"success": True}

@router.delete("/standard/{standard_id}",tags=['standard'],summary="delete a standard")
def standard_delete_particular(request,standard_id):
    std = get_object_or_404(Standard,id=standard_id).delete()
    return JsonResponse({"status":"success","msg":"standard deleted"},status=200)


@router.post("/login",tags=['login'],summary="get login token by username and password",auth=None)
def login(request,body:LoginSchema):
    body = body.dict()
    user = authenticate(username=body['username'],password=body['password'])
    if user:
        payload = {"id":user.id,"class_name":user.student_user.standard.class_name,"full_name":user.student_user.full_name}
        token = jwt.encode(payload,settings.SECRET_KEY,'HS256').decode()
        return JsonResponse({"token":token,"status":"success","msg":"login successfull"},status=200)
    else:
        return JsonResponse({"status":"failed","msg":"incorrect username or password"},status=400)


