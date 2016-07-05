#coding:utf8
import json
import os

from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import Category, SubCategory


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
    elif command =='view':
        data = request_data.get('data')
        categories = Category.objects.all()
        categories_json = []
        for category in categories:
            category_json = dict()
            category_json['name'] = category.name
            category_json['image'] =os.path.join(settings.MEDIA_URL, str(category.image))
            categories_json.append(category_json)

            subcategories_json = []
            subcategories = SubCategory.objects.filter(parent=category)
            for subcategory in subcategories:
                subcategory_json = dict()
                subcategory_json['subcategory_name'] = subcategory.name
                subcategories_json.append(subcategory_json)
            category_json['subcategories'] = subcategories_json

        response['error'] = False
        response['Category'] = categories_json

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