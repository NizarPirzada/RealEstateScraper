import re
import datetime
try:
    from utils import error_responses, helper
except Exception as exp:
    import error_responses
    import helper


def price_validator(price):
    is_valid = 1
    error = ""
    regex = r'\-?\d+\.?\d+'

    if not (re.fullmatch(regex, str(price))):
        is_valid = 0
        error += error_responses.PRICE_IN

    return is_valid, error


def url_validator(url):
    is_valid = 1
    error = ""
    if url == "" or url is None:
        is_valid = 0
        error += error_responses.URL_IN

    return is_valid, error


def supported_website_validator(url):
    is_valid = 1
    error = ""
    supported_website_id = helper.get_supported_website_id(url)
    if supported_website_id == 0:
        is_valid = 0
        error += error_responses.WEBSITE_IN
    return is_valid, error


def real_estate_validator(data):
    is_valid = 1
    error = ""

    if not data['price']:
        is_valid = 0
        error += error_responses.PRICE_IN
    if not data['area']:
        is_valid = 0
        error += error_responses.AREA_IN

    return is_valid, error


def email_validator(is_valid, error, emails):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    resp_emails = []

    for email in emails:
        if re.fullmatch(regex, email):
            resp_emails.append(email)

    if len(resp_emails) == 0:
        is_valid = 0
        error += error_responses.EMAIL_IN
    else:
        resp_emails = ', '.join(resp_emails)
    return is_valid, error, resp_emails


def time_validator(is_valid, error, time_value, time_type):
    regex = r'\d{2}\:\d{2}:\d{2}'
    if not (re.fullmatch(regex, time_value)):
        is_valid = 0
        if time_type == 'start_time':
            error += error_responses.START_TIME_IN
        elif time_type == 'end_time':
            error += error_responses.END_TIME_IN

    return is_valid, error


def time_range_validator(is_valid, error, start_time, end_time):
    start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
    end_time = datetime.datetime.strptime(end_time, '%H:%M:%S')

    if start_time >= end_time:
        is_valid = 0
        error += error_responses.TIME_RANGE_IN

    return is_valid, error


def proxy_validator(is_valid, error, is_proxy):
    proxy_list = [0, 1]
    is_proxy = int(is_proxy)
    if not (is_proxy in proxy_list):
        is_valid = 0
        error += error_responses.IS_PROXY_IN

    return is_valid, error, is_proxy


def websites_details_validator(is_valid, error, websites_data):
    try:
        resp_websites_data = []
        for website_data in websites_data:
            try:
                url = website_data['url']
                desired_price = float(website_data['desired_price'])
                url_valid, _ = url_validator(url)
                supported_website_valid, _ = supported_website_validator(url)
                price_valid, _ = price_validator(desired_price)
                if url_valid and supported_website_valid and price_valid:
                    resp_websites_data.append({
                        "url": url,
                        "desired_price": desired_price
                    })
            except Exception as e:
                print(e)
        if len(resp_websites_data) == 0:
            is_valid = 0
            error += error_responses.WEBSITES_DETAILS

        return is_valid, error, resp_websites_data
    except Exception as exp:
        is_valid = 0
        error += error_responses.WEBSITES_DETAILS
        return is_valid, error, websites_data


def add_configuration_validator(is_valid, error, configurations_data):
    resp_data = {}
    try:
        emails = configurations_data['emails']
        start_time = configurations_data['start_time']
        end_time = configurations_data['end_time']
        is_proxy = configurations_data['is_proxy']
        websites_details = configurations_data['websites_details']
    except Exception as e:
        is_valid = 0
        error += error_responses.KEY_EXP + f'{str(e)}\n'
        return is_valid, error, configurations_data

    is_valid, error, emails = email_validator(is_valid, error, emails)
    is_valid, error = time_validator(is_valid, error, start_time, 'start_time')
    is_valid, error = time_validator(is_valid, error, end_time, 'end_time')
    is_valid, error = time_range_validator(is_valid, error, start_time, end_time)
    is_valid, error, is_proxy = proxy_validator(is_valid, error, is_proxy)
    is_valid, error, websites_details = websites_details_validator(is_valid, error, websites_details)

    if is_valid:
        resp_data = {
            'emails': emails,
            'start_time': start_time,
            'end_time': end_time,
            'is_proxy': is_proxy,
            'websites_details': websites_details
        }

    return is_valid, error, resp_data


def main():
    emails = ["mudasar@gmail.com", "mudasas@dd.cdd"]
    print(email_validator(1, "", emails))
    # print(time_validator(1, '', '11:22', 'end_time'))
    # print(time_range_validator(1, '', '12:11:00', '12:12:00'))
    # print(proxy_validator(1, '', 3))
    # print(price_validator('0.1241241'))
    # data = {
    #     "websites_details" : [
    #         {
    #             "url": "https://www.immobilienscout24.de/Suche/de/nordrhein-westfalen/wohnung-kaufen? \
    #             geocodes=051130000307,0511300007,0511300004,0511300005,055130000100,0511300002,0511300001&sorting=2233",
    #             "desired_price" : 3333
    #         },
    #         {
    #             "url": "https://www.immobilienscout24.de/Suche/de/nordrhein-westfalen/wohnung-kaufen? \
    #             geocodes=051130000307,0511300007,0511300004,0511300005,055130000100,0511300002,0511300001&sorting=2233",
    #             "desired_price": 3333
    #         },
    #         {
    #             "url": "https://stackoverflow.com/questions/17482473/regular-expression-for-price-validation",
    #             "desired_price": 3333
    #         }
    #     ],
    #     "emails": ["mudasar477@gmail.com"],
    #     "start_time": "00:00:00",
    #     "end_time": "23:59:59",
    #     "is_proxy": 1
    # }
    # print(add_configuration_validator(data))


if __name__ == '__main__':
    main()
