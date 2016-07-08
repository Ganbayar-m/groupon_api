# coding=utf-8
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import Sale, Product, Branch, User, Organisation, SubCategory


@api_view(['POST'])
def sale(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        sale = Sale()
        data = request_data.get('data')
        sale.start_date = data.get('start_date')
        sale.finish_date = data.get('finish_date')
        sale.precent = data.get('precent')
        sale.name = data.get('name')
        sale.thumbnail = data.get('thumbnail')
        sale.product = Product.objects.get(id=data.get('product'))
        sale.branch = Branch.objects.get(id=data.get('branch'))
        sale.save()
        response['error'] = False
        response['message'] = 'Амжилттай бүртгэгдлээ.'

    elif command == 'delete':
        data = request_data.get('data')
        sale = Sale.objects.get(id=data.get('id'))
        sale.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа.'

    elif command == 'edit':
        data = request_data.get('data')
        sale = Sale.objects.get(id=data.get('id'))
        sale.start_date = data.get('start_date')
        sale.finish_date = data.get('finish_date')
        sale.precent = data.get('precent')
        sale.name = data.get('name')
        sale.thumbnail = data.get('thumbnail')
        sale.product = Product.objects.get(id=data.get('product'))
        sale.branch = Branch.objects.get(id=data.get('branch'))
        sale.save()
        response['error'] = False
        response['message'] = 'Амжилттай шинэчлэгдлээ.'

    elif command == 'sale_details':
        data = request_data.get('data')
        sales = Sale.objects.filter(id=data.get('sale_id'))
        sales_json = []
        for sale in sales:
            sale_json = dict()
            sale_json['start_date'] = sale.start_date
            sale_json['finish_date'] = sale.finish_date
            sale_json['precent'] = sale.finish_date
            sale_json['id'] = sale.id
            sale_json['product_id'] = sale.product_id
            sale_json['branch_id'] = sale.branch_id
            sale_json['thumbnail'] = os.path.join(settings.MEDIA_URL, str(sale.thumbnail))
            sale_json['name'] = sale.name
            sales_json.append(sale_json)
        response['error'] = False
        response['sales'] = sales_json

    elif command == 'view_all':
        data = request_data.get('data')
        sales = Sale.objects.all()
        sales_json = []
        for sale in sales:
            sale_json = dict()
            sale_json['finish_date'] = sale.finish_date
            sale_json['precent'] = sale.precent
            sale_json['organisation_name'] = sale.branch.organisation.name
            sale_json['id'] = sale.id
            sale_json['thumbnail'] = os.path.join(settings.MEDIA_URL, str(sale.thumbnail))
            sale_json['name'] = sale.name
            sale_json['avatar'] = os.path.join(settings.MEDIA_URL, str(sale.branch.organisation.profile_image))
            sale_json['price'] = sale.price
            sale_json['subcategory_name'] = sale.product.subcategory.name
            sales_json.append(sale_json)

        response['error'] = False
        response['sales'] = sales_json

    elif command == 'view_follow':
        data = request_data.get('data')
        user = User.objects.get(id=data.get('user_id'))
        sales_json = []
        for organisation in user.following_orginisations.all():
            sales = Sale.objects.filter(branch__organisation=organisation)
            for sale in sales:
                sale_json = dict()
                sale_json['finish_date'] = sale.finish_date
                sale_json['precent'] = sale.precent
                sale_json['organisation_name'] = organisation.name
                sale_json['id'] = sale.id
                sale_json['thumbnail'] = os.path.join(settings.MEDIA_URL, str(sale.thumbnail))
                sale_json['name'] = sale.name
                sale_json['avatar'] = os.path.join(settings.MEDIA_URL, str(organisation.profile_image))
                sale_json['price'] = sale.price
                sale_json['subcategory_name'] = sale.product.subcategory.name
                sales_json.append(sale_json)

        response['error'] = False
        response['sale'] = sales_json

    elif command == 'nearby':
        data = request_data.get('data')
        nearbies_json = []
        nearbies = Sale.objects.filter(branch__address__contains=data.get('branch_address'))
        for nearby in nearbies:
            nearby_json = dict()
            nearby_json['finish_date'] = nearby.finish_date
            nearby_json['precent'] = nearby.precent
            nearby_json['organisation_name'] = nearby.branch.organisation.name
            nearby_json['id'] = nearby.id
            nearby_json['thumbnail'] = os.path.join(settings.MEDIA_URL, str(nearby.thumbnail))
            nearby_json['name'] = nearby.name
            nearby_json['avatar'] = os.path.join(settings.MEDIA_URL, str(nearby.branch.organisation.profile_image))
            nearby_json['price'] = nearby.price
            nearby_json['subcategory_name'] = nearby.product.subcategory.name
            nearbies_json.append(nearby_json)

        response['error'] = False
        response['nearby'] = nearbies_json

    elif command == 'view_save':
        data = request_data.get('data')
        sales_json = []
        sales = User.objects.get(pk=data.get('user_id')).save_sale.all()
        for sale in sales:
            sale_json = dict()
            sale_json['finish_date'] = sale.finish_date
            sale_json['precent'] = sale.precent
            sale_json['organisation_name'] = sale.branch.organisation.name
            sale_json['id'] = sale.id
            sale_json['thumbnail'] = os.path.join(settings.MEDIA_URL, str(sale.thumbnail))
            sale_json['name'] = sale.name
            sale_json['avatar'] = os.path.join(settings.MEDIA_URL, str(sale.branch.organisation.profile_image))
            sale_json['price'] = sale.price
            sale_json['subcategory_name'] = sale.product.subcategory.name
            sales_json.append(sale_json)
        response['error'] = False
        response['sales'] = sales_json

    elif command =='save_count':
        data = request_data.get('data')
        sales = User.objects.get(pk=data.get('user_id')).save_sale.all()
        sale_json = dict()
        sale_json['count'] = sales.count()
        response['error'] = False
        response['save'] = sale_json

    elif command == 'save':
        data = request_data.get('data')
        user = User.objects.get(id=data.get('user_id'))
        sale = Sale.objects.get(id=data.get('sale_id'))
        user.save_sale.add(sale)
        response['error'] = False
        response['message'] = 'Хямдралыг хадгаллаа.'
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй.'

    return Response(response)
