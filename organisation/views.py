# -*- coding:utf8 -*-
import json
import os
import user

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from groupon_models.models import Organisation, User, Branch


@api_view(['POST'])
def organisation(request):
    response = dict()

    print request.body

    request_data = json.loads(request.body)
    command = request_data.get('command')  # нэвтэрж орсон эсэхийг шалгах

    if command == 'add':
        data = request_data.get('data')
        if Organisation.objects.filter(name=data.get('name')).exists():
            response['error'] = True
            response['message'] = 'Бүртгэлтэй байгууллага байна.'
        else:
            data = request_data.get('data')
            if Organisation.objects.filter(user = data.get('user')).exists():
                response['error'] = True
                response['message'] = 'Байгуулагт бүртгүүлсэн хэрэглэгч байна.'
            else:
                organisation = Organisation()
                organisation.name = data.get('name')
                organisation.url = data.get('url')
                organisation.user = User.objects.get(id=data.get('user'))
                organisation.cover = data.get('cover')
                organisation.profile_image = data.get('profile_image')
                organisation.save()
                response['error'] = False
                response['message'] = 'Амжилттай бүртгэгдлээ.'

    elif command == 'edit':
        data = request_data.get('data')
        if Organisation.objects.filter(user=data.get('user')).exists():
            response['error'] = True
            response['message'] = 'Байгуулагт бүртгүүлсэн хэрэглэгч байна.'

        else:
            data = request_data.get('data')
            organisation = Organisation.objects.get(id=data.get('id'))
            organisation.name = data.get('name')
            organisation.url = data.get('url')
            organisation.user = User.objects.get(id=data.get('user'))
            organisation.cover = data.get('cover')
            organisation.profile_image = data.get('profile_image')
            organisation.save()
            response['error'] = False
            response['message'] = 'Амжилттай шинэчлэгдлээ.'

    elif command == 'delete':
        data = request_data.get('data')
        organisation = Organisation.objects.get(id=data.get('id'))
        organisation.delete()
        response['error'] = False
        response['message'] = 'Амжилттай устгагдлаа.'

    elif command == 'view':
        data = request_data.get('data')
        user_organisations = Organisation.objects.filter(user_id=data.get('user_id'))
        organisations_json = []
        for user_organisation in user_organisations:
            organisation_json = dict()
            organisation_json['id'] = user_organisation.id
            organisation_json['name'] = user_organisation.name
            organisation_json['url'] = user_organisation.url
            organisation_json['cover'] = os.path.join(settings.MEDIA_URL, str(user_organisation.cover))
            organisation_json['profile_image'] = os.path.join(settings.MEDIA_URL, str(user_organisation.profile_image))
            organisations_json.append(organisation_json)

        response['error'] = False
        response['organisations'] = organisations_json


    elif command == 'view_all':
        data = request_data.get('data')
        organisations = Organisation.objects.all()
        organisations_json = []
        for organisation in organisations:
            organisation_json = dict()
            organisation_json['id'] = organisation.id
            organisation_json['name'] = organisation.name
            organisation_json['url'] = organisation.url
            organisation_json['cover'] = os.path.join(settings.MEDIA_URL, str(organisation.cover))
            organisation_json['profile_image'] = os.path.join(settings.MEDIA_URL, str(organisation.profile_image))
            organisation_json['followers'] = organisation.following.all().count()
            organisation_json['branch'] = organisation.branch_set.all().count()
            # user id ирэхээр follow bol 1 vgvi bol 0
            user_id = User.objects.filter(id = data.get('user_id'))
            organisation_json['follow'] =organisation.following.filter(pk=user_id).exists()
            organisations_json.append(organisation_json)

        response['error'] = False
        response['organisations'] = organisations_json

    elif command == 'follow':
        data = request_data.get('data')
        user = User.objects.get(id=data.get('user_id'))
        organisation = Organisation.objects.get(id=data.get('organisation_id'))
        user.following_orginisations.add(organisation)
        response['error'] = False
        response['message'] = 'Амжилттай follow хийлээ'

    elif command == 'unfollow':
        data = request_data.get('data')
        user = User.objects.get(id=data.get('user_id'))
        organisation = Organisation.objects.get(id=data.get('organisation_id'))
        user.following_orginisations.remove(organisation)
        response['error'] = False
        response['message'] = 'Амжилттай unfollow хийлээ'

    elif command == 'view_organisation':
        data = request_data.get('data')
        user_organisations = Organisation.objects.filter(id=data.get('id'))
        organisations_json = []
        for user_organisation in user_organisations:
            organisation_json = dict()
            organisation_json['name'] = user_organisation.name
            organisation_json['url'] = user_organisation.url
            organisation_json['cover'] = os.path.join(settings.MEDIA_URL, str(user_organisation.cover))
            organisation_json['profile_image'] = os.path.join(settings.MEDIA_URL, str(user_organisation.profile_image))
            organisation_json['description'] = user_organisation.description
            organisation_json['followers'] = user_organisation.following.all().count()
            organisation_json['branch'] = user_organisation.branch_set.all().count()
            organisations_json.append(organisation_json)

        branchs_json = []
        for organisation in Organisation.objects.filter(id=data.get('id')):
            branchs = Branch.objects.filter(organisation_id=organisation)
            for branch in branchs:
                branch_json = dict()
                branch_json['name'] = branch.name
                branch_json['phone_number'] = branch.phone_number
                branch_json['profile_image'] = os.path.join(settings.MEDIA_URL, str(branch.profile_image))
                branch_json['sales'] = branch.sale_set.all().count()
                branchs_json.append(branch_json)

        organisation_json['branchs'] = branchs_json
        response['error'] = False
        response['organisations'] = organisations_json
    else:
        response['error'] = True
        response['message'] = 'Комманд олдсонгүй.'
    return Response(response)


