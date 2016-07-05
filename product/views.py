# -*- coding:utf8 -*-

import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import Product, User, SubCategory


@api_view(['POST'])
def product(request):

    response = dict()
    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        data = request_data.get('data')
        if Product.objects.filter(name=data.get('name')).exists():
            response['error'] = True
            response['message'] = 'Барааны нэр давхцаж байна.'
        else:
            product= Product()
            product.name = data.get('name')
            product.price = data.get('price')
            product.details = data.get('details')
            product.rating = data.get('rating')
            product.user = User.objects.get(id=data.get('user'))
            product.subcategory = SubCategory.objects.get(id=data.get('subcategory'))
            product.save()
            response['error'] = False
            response['message'] = 'Амжилттай нэмэгдлээ.'

    elif command == 'delete':
        data= request_data.get('data')
        product = Product.objects.get(id=data.get('id'))
        product.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа.'

    elif command == 'view_all':
        data = request_data.get('data')
        products = Product.objects.all()
        products_json = []
        Product.objects.filter(subcategory_id=data.get('subcategory_id'))
        for product in products:
                product_json = dict()
                product_json ['name'] = product.name
                product_json ['price'] = product.price
                product_json ['details'] = product.details
                product_json ['rating'] = product.rating
                products_json.append(product_json)

        response['error'] = False
        response['products'] = products_json
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй.'

    return Response(response)

