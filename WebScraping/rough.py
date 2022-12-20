# import requests
# import time
# from bs4 import BeautifulSoup
# from bs4 import Tag
# from utils import dbhelper, validator, helper
# from utils.table_names import TableName
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import ssl
# # url = "https://www.immowelt.de/liste/berlin/wohnungen/kaufen?d=true&sd=DESC&sf=RELEVANCE&sp=4"
#
# headers = {
#     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
#         Chrome/51.0.2704.103 Safari/537.36"
# }
# seconds = 20
# base_url = 'https://www.ebay-kleinanzeigen.de'
# def send_gmail(data):
#     is_success = 1
#     error = ""
#
#     try:
#         sender_email = "realestateemail512@gmail.com"
#         password = 'realpassword'
#
#         emails = data['emails']
#         # url = data['url']
#         # per_square_area_price = data['per_square_area_price']
#
#         message = MIMEMultipart('text')
#         message["Subject"] = data['subject']
#         message["From"] = sender_email
#         message["To"] = emails
#
#         # Turn these into plain/html MIMEText objects
#         part2 = MIMEText(data['html'], "html")
#
#         # Add HTML/plain-text parts to MIMEMultipart message
#         # The email client will try to render the last part first
#         message.attach(part2)
#
#         emails = emails.split(',')
#         # Create secure connection with server and send email
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(
#                 sender_email, emails, message.as_string()
#             )
#
#     except Exception as exp:
#         is_success = 0
#         error = f"Error while sending alert: {exp}"
#         print(error)
#     return is_success, error
#
# def calculate_per_square_price(price, area):
#     try:
#         per_square_price = float(price)/float(area)
#     except Exception as e:
#         print("Per Square Price calculation error:", e)
#         per_square_price = 111111
#     return per_square_price
#
# def create_email_template(site_url, result, website_id):
#     table_name = TableName.REAL_ESTATE
#     last_inserted_real_estate_id = dbhelper.get_last_id(table_name)
#
#     # for item in real_estate_data_scraped:
#     desired_price = 100000
#     is_good = 0
#     # email_sent = 0
#
#     html = """\<h3>Page URL: %s</h3>
#             <table border='1'>
#                     <tr>
#                         <th>Sr.No</th>
#                         <th>URL</th>
#                         <th>Area Price Per Square</th>
#                     </tr>
#            """ % (site_url)
#     i = 1
#     temp = []
#     for item in result:
#
#         url = item['url']
#         file_path = item['file_path']
#         is_success, error = validator.real_estate_validator(item)
#         if is_success:
#             per_square_price = calculate_per_square_price(item['price'], item['area'])
#             dup_real_estate_list = dbhelper.get_duplicate_real_estate(url)
#             is_unique = helper.check_duplicate_real_estate(item, dup_real_estate_list)
#             if is_unique:
#                 if per_square_price < desired_price:
#                     is_good = 1
#
#                     html = html + "<tr>"
#                     html = html + "<td>" + str(i) + "</td>"
#                     html = html + "<td>" + item['url'] + "</td>"
#                     html = html + "<td>" + str(int(per_square_price)) + "</td>"
#                     html = html + "</tr>"
#             email_sent =0
#             real_estate_data = [last_inserted_real_estate_id + i, url, file_path, item['price'], item['area'],
#                                 is_good, email_sent, website_id]
#             temp.append(real_estate_data)
#         else:
#             print(error)
#         i+=1
#
#     html = html + "</table>"
#     email_data = {
#         'emails': "azazrashid797@gmail.com",
#         'subject': "Alert - New Real Estate",
#         'html': html
#     }
#
#     is_success, error = send_gmail(email_data)
#     # if is_success:
#     #     email_sent = 1
#
#     for each in temp:
#         if is_success:
#             each[6] = 1
#         last_inserted_real_estate_id = dbhelper.insert_real_estate(each)
#
#     tz = pytz.timezone('Europe/Berlin')
#     updated_website_data = {
#         'website_id': website_id,
#         'iter_no': iter_no + 1,
#         'error_creation_datetime': datetime.datetime.now(tz)
#     }
#     dbhelper.update_record(TableName.WEBSITE, updated_website_data)
#
# def convert_codes_to_html(html):
#     html = str(html)
#     html = html.replace("&lt;", '<')
#     html = html.replace("&gt;", '>')
#     html = BeautifulSoup(html, 'html.parser')
#     return html
#
# def scrape_real_estate(url, is_proxy=0):
#     data = []
#     proxy = None
#     if is_proxy:
#         proxy = {
#             "https": helper.get_random_proxy()
#         }
#     page = requests.get(url, headers=headers, timeout=time.sleep(seconds), proxies=proxy)
#     soup = BeautifulSoup(page.content, "html.parser")
#     soup = helper.convert_codes_to_html(soup)
#     real_estates_ul = soup.find(id="srchrslt-adtable")
#
#     for item in real_estates_ul.findAll('li', class_=["lazyload-item"]):
#         real_estate_object = {}
#         if isinstance(item, Tag):
#             try:
#                 article = item.find('article')
#                 try:
#                     real_estate_object['url'] = base_url + article['data-href']
#                 except:
#                     real_estate_object['url'] = None
#                 try:
#                     price = item.find("p", {"class": "aditem-main--middle--price"}).contents[0].strip()
#                     # price = re.findall('\d*\.?\d+', price)[0]
#                     price = price.split(' ')[0]
#                     price = price.replace('.', '')
#                     price = price.replace(',', '')
#                     price = int(price)
#                     real_estate_object['price'] = price
#                 except Exception as e:
#                     print('price error:', e)
#                     real_estate_object['price'] = None
#                 try:
#                     area = item.findAll("span", {"class": "simpletag tag-small"})[0].contents[0].strip()
#                     # area = re.findall('\d*\.?\d+', area)[0]
#                     area = area.split(' ')[0]
#                     area = float(area.replace(',', '.'))
#                     real_estate_object['area'] = area
#                 except Exception as e:
#                     print('area error:', e)
#                     real_estate_object['area'] = None
#                 real_estate_object['file_path'] = ""
#
#                 data.append(real_estate_object)
#
#             except Exception as e:
#                 print('e', e)
#                 # print(item.prettify())
#             # break
#     return data
#
# url_ = "https://www.ebay-kleinanzeigen.de/s-wohnung-kaufen/berlin/seite:50/c196l3331"
# result = scrape_real_estate(url_, is_proxy=0)
#
# create_email_template(url_, result, website_id=1)

st = "2021-10-26 16:43:28"

# from datetime import datetime
# now = datetime.now()
# prev = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
# x = datetime.now()
#
# diff = x - prev
#
# total_seconds = diff.seconds
# minutes = total_seconds//60
# print(diff)
import time
from pathlib import Path
from bs4 import BeautifulSoup
from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from utils import helper, dbhelper
from utils.table_names import TableName
import traceback
from anticaptchaofficial.geetestproxyless import *

# profile = webdriver.FirefoxProfile()
driver = webdriver.Firefox()
driver.get("https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?enteredFrom=result_list")
solver = geetestProxyless()
solver.set_verbose(1)
solver.set_key("be53d62b18b765854ecd3d8e3e930adb")
solver.set_website_url("https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?enteredFrom=result_list")
solver.set_gt_key(input())
solver.set_challenge_key(input())


token = solver.solve_and_return_solution()
if token != 0:
    print("result tokens: ")
    print(token)
else:
    print("task finished with error "+solver.error_code)