from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from utils.table_names import TableName
from utils import dbhelper, error_responses


def index(request):
    return render(request, 'settings.html')


@api_view(["GET", "POST", "PUT", "DELETE"])
def settings(request):
    try:

        if request.method == "GET":
            data = dbhelper.get_all_data(TableName.SETTING)
            data = data[::-1][0]

            return Response(data, status.HTTP_200_OK)
        elif request.method == "POST":
            data = json.loads(request.body)
            captcha_string = data['captcha_string']

            if captcha_string == '' or not captcha_string:
                return Response(error_responses.CAPTCHA_IN, status.HTTP_400_BAD_REQUEST)

            last_row_id = dbhelper.get_last_id(TableName.SETTING) + 1

            # for configurations (row_id, captcha_string)
            settings_data = (last_row_id, captcha_string)
            _ = dbhelper.insert_setting(settings_data)

            return Response("Success", status.HTTP_200_OK)

    except ValueError as e:
        print("Error: ", e)
        return Response("Invalid data provided", status.HTTP_400_BAD_REQUEST)
