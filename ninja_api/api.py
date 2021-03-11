from ninja import NinjaAPI, Router, Schema
from ninja.orm import create_schema
from django.http import JsonResponse
from exam.models import Questions, Standard, Student, User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

class StandardSchema(Schema):
    class_name:str


class StandardSerializer(ModelSerializer):
    class Meta:
        model = Standard
        fields = "__all__"

router = Router()

@router.get("/standard",tags=['standard'],summary="get list of standards")
def standard_get(request):
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
    return JsonResponse({"status":"success","msg":"standard deleted"},status=201)

