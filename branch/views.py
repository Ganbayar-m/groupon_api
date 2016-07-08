# coding:utf8
import json
import os

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_api import settings
from groupon_models.models import Branch, Organisation, Product


@api_view(['POST'])
def branch(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'view':
        data = request_data.get('data')
        branchs_json = []
        for organisation in Organisation.objects.filter(id=data.get('id')):
            branchs = Branch.objects.filter(organisation_id=organisation)
            for branch in branchs:
                branch_json = dict()
                branch_json['phone_number'] = branch.phone_number
                branch_json['address'] = branch.address
                branch_json['location'] = branch.location
                branch_json['profile_image'] = os.path.join(settings.MEDIA_URL, str(branch.profile_image))
                branchs_json.append(branch_json)
        response['error'] = False
        response['message'] = branchs_json

    if command == 'details':
        data = request_data.get('data')
        branch = Branch.objects.get(id=data.get('id'))
        branch_json = dict()
        branch_json['phone_number'] = branch.phone_number
        branch_json['address'] = branch.address
        branch_json['location'] = branch.location
        branch_json['description'] = branch.description
        branch_json['url'] = branch.organisation.url
        branch_json['name'] = branch.name
        branch_json['profile_image'] = os.path.join(settings.MEDIA_URL, str(branch.profile_image))
        branch_json['cover'] = os.path.join(settings.MEDIA_URL, str(branch.cover))

        products = branch.product.all()

        products_json = []
        for product in products:
            product_json = dict()
            product_json['picture'] = os.path.join(settings.MEDIA_URL, str(product.picture))
            product_json['name'] = product.name
            product_json['price'] = product.price
            products_json.append(product_json)
        branch_json['products'] = products_json

        response['error'] = False
        response['Branch'] = branch_json
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй'

    return Response(response)
