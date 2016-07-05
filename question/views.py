#coding:utf8
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import Question, Sale, User


@api_view(['POST'])
def question(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        question = Question()
        data = request_data.get('data')
        question.question = data.get('question')
        question.sale = Sale.objects.get(id=data.get('sale'))
        question.user = User.objects.get(id=data.get('user'))
        question.save()

        response['error'] = False
        response['message'] = 'Амжилттай нэмэгдлээ'

    elif command == 'edit':
        data = request_data.get('data')
        question = Question.objects.get(id=data.get('id'))
        question.question = data.get('question')
        question.sale = Sale.objects.get(id=data.get('sale'))
        question.user = User.objects.get(id=data.get('user'))
        question.save()
        response['error'] = False
        response['message'] = 'Амжилттай шинэчлэгдлээ.'

    elif command == 'delete':
        data = request_data.get('data')
        question = Question.objects.get(id=data.get('id'))
        question.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа.'
    else:
        response['error'] = True
        response['message'] ='Комманд олдсонгүй'

    return Response(response)