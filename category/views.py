#coding:utf8
import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import Category


@api_view(['POST'])
def category(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        data = request_data.get('data')
        if Category.objects.filter(name=data.get('name')).exists():
            response['error'] = True
            response['message'] = 'Ангилалын нэр давхардаж байна.'
        else:
            category = Category()
            data = request_data.get('data')
            category.name = data.get('name')
            category.save()
            response['error'] = False
            response['message'] = 'Амжилттай нэмэгдлээ'
    elif command == 'edit':
        data = request_data.get('data')
        if Category.objects.filter(name = data.get('name')).exists():
            response['error'] = True
            response['message'] = 'Ангилалын нэр давхардаж байна.'
        else:
            category = Category()
            data = request_data.get('data')
            category = Category.objects.get(id=data.get('id'))
            category.name = data.get('name')
            category.save()
            response['error'] = False
            response['message'] = 'Амжилттай шинэчлэгдлээ.'
    elif command =='delete':
        data = request_data.get('data')
        category = Category.objects.get(id=data.get('id'))
        category.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа'
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй'

    return Response(response)