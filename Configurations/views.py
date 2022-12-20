from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from utils.table_names import TableName
from utils import dbhelper, helper, validator, error_responses


def index(request):
    return render(request, 'index.html')


@api_view(["GET", "POST", "PUT", "DELETE"])
def configurations(request):
    try:

        if request.method == "GET":
            data = []
            configurations_data = dbhelper.get_all_data(TableName.CONFIGURATION)
            for configuration in configurations_data:
                configurations_data = \
                    {'configuration_id': configuration['configuration_id'],
                   'created_date': configuration['created_date'],
                   'emails': configuration['emails'],
                   # 'start_time': helper.convert_datetime_timezone(time=configuration['start_time'],
                   #                                                tz1="UTC",
                   #                                                tz2="Europe/Berlin"),
                   'start_time': configuration['start_time'],
                   # 'end_time': helper.convert_datetime_timezone(time=configuration['end_time'],
                   #                                              tz1="UTC",
                   #                                              tz2="Europe/Berlin"),
                   'end_time': configuration['end_time'],
                   'is_proxy': configuration['is_proxy'],
                   # 'execution_status':  helper.is_time_between(configuration['start_time'], configuration['end_time']) ,
                   'execution_status': helper.calculate_execution_status(configuration['active_state'],
                                                                         helper.is_datetime_between(configuration['start_time'], configuration['end_time'], "time")),

                   'active_state': configuration['active_state']}

                website_data = dbhelper.get_data_by_parent_id(TableName.WEBSITE, TableName.CONFIGURATION,
                                                              configuration['configuration_id'])
                websites_details = []
                for website in website_data:
                    website_details = {'website_id': website['website_id']}
                    is_valid, _ = validator.url_validator(website['url'])
                    if not is_valid:
                        continue
                    website_details['url'] = website['url']
                    website_details['desired_price'] = website['desired_price']
                    # configurations_data['configuration_details'].append(website_details)
                    websites_details.append(website_details)

                if len(websites_details) == 0:
                    continue
                configurations_data['websites_details'] = websites_details
                # print(configurations_data)
                data.append(configurations_data)
            data = data[::-1]

            return Response(data, status.HTTP_200_OK)

        elif request.method == "POST":
            is_valid = 1
            error = ''
            data = json.loads(request.body)
            print(data)
            is_valid, validation_error, resp_data = validator.add_configuration_validator(is_valid, error, data)

            if not is_valid:
                error += error_responses.DATA_IN
                error += validation_error
                return Response(error, status.HTTP_400_BAD_REQUEST)

            data = resp_data

            table_name = TableName.CONFIGURATION
            last_row_id = dbhelper.get_last_id(table_name) + 1
            emails = data['emails']
            # start_time = helper.convert_datetime_timezone(time=data['start_time'])
            start_time = data['start_time']
            # end_time = helper.convert_datetime_timezone(time=data['end_time'])
            end_time = data['end_time']

            is_proxy = data['is_proxy']
            # for configurations (row_id, emails comma separated, start_time, end_time)
            configuration_data = (last_row_id, emails, start_time, end_time, is_proxy)
            last_inserted_configuration_id = dbhelper.insert_configuration(configuration_data)

            if last_inserted_configuration_id > 0:

                websites_details = data['websites_details']
                last_inserted_website_id = dbhelper.get_last_id(TableName.WEBSITE)

                for website_details in websites_details:
                    url = website_details['url']
                    desired_price = website_details['desired_price']

                    supported_website_id = helper.get_supported_website_id(url)
                    if supported_website_id > 0:
                        # for websites (row_id, url, desired_price, supported_website_id, configuration_id)
                        website_data = (last_inserted_website_id+1, url, float(desired_price), supported_website_id,
                                        last_inserted_configuration_id)
                        last_inserted_website_id = dbhelper.insert_website(website_data)
                    else:
                        print(f'{url} is not is our support list.')
            else:
                print('Error while inserting data:', configuration_data)
            return Response("Success", status.HTTP_200_OK)

        elif request.method == "PUT":
            data = json.loads(request.body)
            print(data)

            dbhelper.update_record(TableName.CONFIGURATION, data)
            return Response("Success", status.HTTP_200_OK)

    except ValueError as e:
        print("Error: ", e)
        return Response("Invalid data provided", status.HTTP_400_BAD_REQUEST)
