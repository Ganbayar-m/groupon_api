#coding:utf8
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groupon_models.models import Answer, Question


@api_view(['POST'])
def answer(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'add':
        answer = Answer()
        data = request_data.get('data')
        answer.answer = data.get('answer')
        answer.question = Question.objects.get(id=data.get('question'))
        answer.save()
        response['error'] = False
        response['message'] = 'Амжилттай нэмэгдлээ'

    elif command == 'edit':
        data = request_data.get('data')
        answer = Answer.objects.get(id=data.get('id'))
        answer.answer = data.get('answer')
        answer.question = Question.objects.get(id=data.get('question'))
        answer.save()
        response['error'] = False
        response['message'] = 'Амжилттай шинэчлэгдлээ.'

    elif command == 'delete':
        data = request_data.get('data')
        answer = Answer.objects.get(id=data.get('id'))
        answer.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа.'

    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй'

    return Response(response)