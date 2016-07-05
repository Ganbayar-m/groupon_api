#coding:utf8
import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import SubCategory, Category


@api_view(['POST'])
def subcategory(request):
    response = dict()

    print request.body

    request_data=json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        subcategory = SubCategory()
        data = request_data.get('data')
        subcategory.name = data.get('name')
        subcategory.parent = Category.objects.get(id=data.get('id'))
        subcategory.save()
        response['error'] = False
        response['message'] = 'Амжилттай нэмэгдлээ'
    elif command == 'delete':
        data = request_data.get('data')
        subcategory = SubCategory.objects.get(id=data.get('id'))
        subcategory.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа'
    elif command =='edit':
        data = request_data.get('data')
        subcategory = SubCategory.objects.get(id=data.get('id'))
        subcategory.name = data.get('name')
        subcategory.parent = Category.objects.get(id=data.get('id'))
        subcategory.save()
        response ['error'] = False
        response ['message'] = 'Амжилттай шинэчлэгдлээ'
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй'

    return Response(response)