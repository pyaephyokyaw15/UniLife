# from rest_framework.renderers import BaseRenderer
from rest_framework import renderers
from rest_framework.utils import json
import re


def status_code_mapper(status_code):
    # map common HTTP status codes to message
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
    return message


class CustomRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):  # override the render method.
        # print(data)
        # print(str(data))
        # print(renderer_context['response'])
        status_code = renderer_context['response'].status_code
        message = status_code_mapper(status_code)

        if data.get('detail'):  # check whether there is an error or not
            response = json.dumps({'result': None, 'errors': data, 'status_code': status_code, 'message': message})
        else:
            result = dict()
            if data.get('results'):
                # check whether pagination is used
                # if pagination is used, data dict has 'results' key and store data in it.

                result['data'] = data['results']

                pagination = dict()
                # pagination["count"] = data["count"]

                page_regex = re.compile(r'.*page=(\d+)')  # regex to retrieve only page number

                next_page_url = data["next"]
                if next_page_url:
                    next_page_id_search = page_regex.search(next_page_url)
                    next_page_id = int(next_page_id_search.group(1))
                else:
                    next_page_id = None

                previous_page_url = data["previous"]
                if previous_page_url:
                    previous_page_id_search = page_regex.search(previous_page_url)
                    if previous_page_id_search:
                        previous_page_id = int(previous_page_id_search.group(1))
                    else:
                        # if page=1, page query is not included in url.
                        # Using regex, group() method will throw an error.
                        # So, avoid this method and assign 1 to id.
                        previous_page_id = 1
                else:
                    previous_page_id = None

                pagination["next_page"] = next_page_id
                pagination["previous_page"] = previous_page_id

                result['pagination'] = pagination

            else:
                # if pagination is not used,
                result = data

            response = json.dumps({'result': result, 'status_code': status_code,
                                   'message': message})
        return response


# class CustomApiRenderer(renderers.JSONRenderer):
#     charset = 'utf-8'
#
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         response = ''
#         print(data)
#         print(renderer_context['response'])
#         status_code = renderer_context['response'].status_code
#         message = status_code_mapper(status_code)
#
#         if 'ErrorDetail' in str(data):
#             if status_code == 404:
#                 response = json.dumps({'result': None, 'status_code': status_code, 'message': message})
#             else:
#                response = json.dumps({'result': None, 'errors': data, 'status_code': status_code, 'message': message})
#         else:
#             response = json.dumps({'result': data, 'status_code': status_code, 'message': message})
#     return response
