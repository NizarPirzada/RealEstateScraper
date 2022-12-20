import datetime
import time
import os
from dateutil import parser
import pytz
from utils import dbhelper, validator, helper
from utils.table_names import TableName
from WebScraping import scrapper
import traceback
import uuid

def process_website(data=None):
    if data is None:
        data = {}
    print(data)
    try:
        website_id = data['website_id']
        # configurations_data = dbhelper.get_data_by_id(TableName.CONFIGURATION, data[TableName.CONFIGURATION+'_id'])
        desired_price = float(data['desired_price'])
        emails = data['emails']

        supported_website_id = data['supported_website_id']
        website_url = data['url']
        iter_no = data['iter_no']
        is_proxy = data['is_proxy']
        # real_estate_data_scraped = []
        real_estate_data_scraped = scrapper.main(data)
        if len(real_estate_data_scraped) < 5:
            updated_website_data = {
                'website_id': website_id
            }
            last_error_datetime = data['last_error_datetime']
            if last_error_datetime:
                start_time = parser.parse(last_error_datetime)
                end_time = start_time + datetime.timedelta(hours=4)
                start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
                end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                is_send_alert = int(not helper.is_datetime_between(start_time, end_time, "datetime"))
            else:
                is_send_alert = 1
                # tz = pytz.timezoneupdated_website_data('Europe/Berlin')
                # ['error_creation_datetime'] = datetime.datetime.now(tz)

            if is_send_alert:
                error_creation_datetime = data['error_creation_datetime']
                if not error_creation_datetime:
                    error_creation_datetime = "--/--"
                email_id = str(uuid.uuid4())[:8]
                html = """\
                        <html>
                        <body>
                            <h4>
                            No data while scraping website
                            </h4>
                            <p>
                            Website Id : %s
                            </p>
                            <p>
                            URL : %s
                            </p>
                            <p>
                            Last successfully run at : %s
                            </p
                             <p>
                            Process Id: %s
                            </p>
                        </body>
                        </html>
                        """ % (str(website_id), website_url, error_creation_datetime, email_id)
                email_data = {
                    'emails': emails,
                    'subject': f"Alert - No data while scraping website.",
                    'html': html
                }
                msg = f"No Data found while scraping website: Website Id:{str(website_id)} URL: {website_url} Last " \
                      f"successfully run at:{error_creation_datetime} "
                helper.log_summary((website_url, website_id), msg)
                is_success, error = helper.send_gmail(email_data)
                try:
                    if is_success:
                        log_summary((website_url, website_id), f"Email Sent. Process Id:{email_id}")
                except:
                    pass
                tz = pytz.timezone('Europe/Berlin')
                updated_website_data['last_error_datetime'] = datetime.datetime.now(tz)

                dbhelper.update_record(TableName.WEBSITE, updated_website_data)
            # return

        tz = pytz.timezone('Europe/Berlin')
        updated_website_data = {
            'website_id': website_id,
            'iter_no': iter_no+1,
            'error_creation_datetime': datetime.datetime.now(tz)
        }
        dbhelper.update_record(TableName.WEBSITE, updated_website_data)
    except Exception as e:
        helper.log_errors(e)


def listener():
    while True:
        try:
            websites_data = dbhelper.get_scheduled_websites()
            for data in websites_data:
                helper.log_summary((data['url'], data['website_id']), f"Processing the following configuration:{data}")
                process_website(data)
                # TODO call multi thread function where we scrap the link and do the real estate analyzing
            os.system("tskill firefox")
        except Exception as e:
            print("Error in main function:", e)

            pass
        # break
        time.sleep(50)
        print("ss")


if __name__ == '__main__':
    database = r"real_estate.sqlite3"
    listener()
