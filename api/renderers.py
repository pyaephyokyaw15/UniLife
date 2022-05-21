from rest_framework import renderers
from rest_framework.utils import json
import re


class CustomApiRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):  # override the render method.
        # print('Data', data)
        # print('Context', renderer_context['request'])
        method = renderer_context['request'].method
        # print('string Data', str(data))
        # print('render_context', renderer_context)
        # print(renderer_context['response'])

        result = None
        status_code = renderer_context['response'].status_code
        message = ''

        if data:  # for not delete cases. (in delete case, there is no response data)
            error_message = data.get('detail')
            # print("In here")

            if error_message:  # if there is an error, return null and error code
                response = json.dumps({'result': result, 'status_code': status_code, 'message': error_message})
                return response
            else:  # if there is no error
                # map message according to status_code and frontend requirement
                if status_code == 200:
                    if method == 'PUT':
                        message = 'Successfully Updated'
                    else:
                        message = 'OK'
                elif status_code == 201:
                    message = 'Successfully Created'
                elif status_code == 202:
                    message = 'Accepted'
                elif status_code == 204:
                    message = 'Successfully Deleted'

                # result
                if 'ErrorDetail' in str(data):  # if there is an exception, assign data into message
                    # print(data)
                    # print(data.values())
                    # message = data
                    message_list = list(data.values())[0]  # convert order_dict to list
                    message = '\n'.join(message_list)
                else:  # if there is no exception, assign data into result
                    result = dict()
                    if 'results' in data:
                        # check whether pagination is used
                        # if pagination is used, data dict has 'results' key and store data in it.

                        # print('Results:', data['results'])
                        result['data'] = data['results']

                        pagination = dict()

                        pagination["total_pages"] = data["total_pages"]
                        pagination["current_page"] = data["current_page"]
                        pagination["next_page"] = data["next_page"]
                        pagination["previous_page"] = data["previous_page"]

                        result['pagination'] = pagination

                    else:
                        # if pagination is not used,
                        result = data
        else:   # there is no response data.(delete case)
            message = 'Successfully deleted'
        response = json.dumps({'result': result, 'status_code': status_code, 'message': message})
        return response


# class CustomAuthApiRenderer(renderers.JSONRenderer):
#     charset = 'utf-8'
#
#     def render(self, data, accepted_media_type=None, renderer_context=None):  # override the render method.
#         print('Data', data)
#         print('Context', renderer_context['request'])
#         print('Test', data)
#         print(type(data))
#         print('Test', list(data.values()))
#         # print('string Data', str(data))
#         # print('render_context', renderer_context)
#         # print(renderer_context['response'])
#
#         status_code = renderer_context['response'].status_code
#         result = None
#
#         error_message = data.get('detail')
#
#         if error_message:  # if there is an error
#             response = json.dumps({'result': result, 'status_code': status_code, 'message': error_message})
#
#         else:
#             if 'ErrorDetail' in str(data):  # if there is an exception, assign data into message
#                 message_list = list(data.values())[0]
#                 message = '\n'.join(message_list)
#
#             else:  # if there is no exception, assign data into result
#                 result = data
#                 message = 'OK'
#
#             response = json.dumps({'result': result, 'status_code': status_code, 'message': message})
#         return response


