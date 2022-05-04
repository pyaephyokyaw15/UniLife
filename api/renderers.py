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


