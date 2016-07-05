#coding:utf8
import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import UserReview, User, Product


@api_view(['POST'])
def user_review(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        user_review = UserReview()
        data = request_data.get('data')
        user_review.rating = data.get('rating')
        user_review.comment = data.get('comment')
        user_review.user = User.objects.get(id=data.get('user'))
        user_review.product = Product.objects.get(id=data.get('product'))
        user_review.save()
        response['error'] = False
        response['message'] = 'Амжилттай нэмэгдлээ'

    elif command == 'edit':
        data = request_data.get('data')
        user_review = UserReview.objects.get(id=data.get('id'))
        user_review.rating = data.get('rating')
        user_review.comment = data.get('comment')
        user_review.user = User.objects.get(id=data.get('user'))
        user_review.product = Product.objects.get(id=data.get('product'))
        user_review.save()
        response['error'] = False
        response['message'] = 'Амжилттай шинэчлэгдлээ'

    elif command == 'delete':
        data = request_data.get('data')
        user_review = UserReview.objects.get(id=data.get('id'))
        user_review.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа'
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй'
    return Response(response)