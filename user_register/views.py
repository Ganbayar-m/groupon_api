# -*- coding: utf-8 -*-
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from groupon_models.models import User


@api_view(['POST'])
def user_register(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')

    if command == 'register':
        data = request_data.get('data')
        if User.objects.filter(email=data.get('email')).exists():
            response['error'] = True
            response['message'] = 'Бүртгэлтэй хэрэглэгч байна.'
        else:
            user = User()
            data = request_data.get('data')
            user.email = data.get('email')
            user.password = data.get('password')
            user.firstname = data.get('firstname')
            user.lastname = data.get('lastname')
            # bvrtgvvleheer defaultaar zurag uguh
            user.save()
            response['error'] = False
            response['message'] = 'Амжилттай бүртгэгдлээ.'

    elif command == 'login':
        data = request_data.get('data')
        try:
            user = User.objects.get(email=data.get('email'))
            if user.password == data.get('password'):
                data = request_data.get('data')
                users = User.objects.filter(email=data.get('email'))
                users_json = []
                for user in users:
                    user_json = dict()
                    user_json['id'] = user.id
                    user_json['email'] = user.email
                    user_json['password'] = user.password
                    user_json['lastname'] = user.lastname
                    user_json['firstname'] = user.firstname
                    user_json['image'] = os.path.join(settings.MEDIA_URL, str(user.image))
                    users_json.append(user_json)
                response['users'] = users_json
                response['error'] = False
                response['message'] = 'Амжилтай нэвтэрлээ'


            else:
                response['error'] = True
                response['message'] = 'Нууц үг, имэйл буруу байна.'
        except User.DoesNotExist:
            response['error'] = True
            response['message'] = 'Нууц үг, имэйл буруу байна.'
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй.'
    return Response(response)

