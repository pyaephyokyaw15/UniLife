# from rest_framework.renderers import BaseRenderer
from rest_framework import renderers
from rest_framework.utils import json


class ApiRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        print(data)
        print(renderer_context['response'])
        status_code = renderer_context['response'].status_code

        if status_code == 200:
            message = 'OK'
        elif status_code == 201:
            message = 'Created'
        elif status_code == 202:
            message = 'Accepted'
        elif status_code == 204:
            message = 'No Content'
        elif status_code == 400:
            message = 'Bad Request'
        elif status_code == 403:
            message = 'Forbidden'
        elif status_code == 404:
            message = 'Not Found'
        elif status_code == 405:
            message = 'Method Not Allowed'
        else:
            message = "Error"

        if 'ErrorDetail' in str(data):
            if status_code == 404:
                response = json.dumps({'result': None, 'status_code': status_code, 'message': message})
            else:

                response = json.dumps({'result': None, 'errors': data, 'status_code': status_code, 'message': message})
        else:
            response = json.dumps({'result': data, 'status_code': status_code, 'message': message})

        return response


class ApiPaginationRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        print(data)
        print(renderer_context['response'])
        status_code = renderer_context['response'].status_code

        if status_code == 200:
            message = 'OK'
        elif status_code == 201:
            message = 'Created'
        elif status_code == 202:
            message = 'Accepted'
        elif status_code == 204:
            message = 'No Content'
        elif status_code == 400:
            message = 'Bad Request'
        elif status_code == 403:
            message = 'Forbidden'
        elif status_code == 404:
            message = 'Not Found'
        elif status_code == 405:
            message = 'Method Not Allowed'
        else:
            message = "Error"

        if status_code == 404:
            response = json.dumps({'result': None, 'status_code': status_code, 'message': message})
        else:
            result = dict()
            result['data'] = data['results']
            pagination = dict()
            # pagination["count"] = data["count"]
            pagination["next"] = data["next"]
            pagination["previous"] = data["previous"]
            result['pagination'] = pagination
            response = json.dumps({'result': result, 'status_code': status_code,
                                   'message': message})

        return response

