import requests
import time
from bs4 import BeautifulSoup
from bs4 import Tag
from utils import helper
from fake_useragent import UserAgent
import traceback

seconds = 15
base_url = 'https://www.ebay-kleinanzeigen.de'


def get_page_urls(url, website_id, urls=[], is_proxy=0, counter=1): #        iter_no = 0
    try:
        proxy = None
        if is_proxy:
            proxy = {
                "https": helper.get_random_proxy()
            }
        seconds = helper.get_random_number(20, 30)
        useragent = UserAgent(use_cache_server=False)
        headers = {'User-Agent': useragent.random}
        page = requests.get(url, headers=headers, timeout=seconds, proxies=proxy)
        soup = BeautifulSoup(page.content, "html.parser")
        soup = helper.convert_codes_to_html(soup)
        pagination = soup.find("div", {"class": "pagination-pages"})

        paginations = pagination.findAll('a', {"class": "pagination-page"})
        # if iter_no > 0:
        #     for item in paginations[:2]:
        #         if (base_url + item['href']) not in urls:
        #             urls.append(base_url + item['href'])
        #     return urls
        # else:
        for item in paginations:
            if (base_url + item['href']) not in urls:
                urls.append(base_url + item['href'])
        # print(base_url + x['href'])
        # if (base_url + x['href']) == url:
        last_page = paginations[-1].text.strip()
        print(last_page)
        last_page = int(last_page) + 1
        current_page = soup.find("span", {"class": "pagination-current"})
        if last_page != int(current_page.text):
            urls = get_page_urls(urls[-1], website_id, urls, 0)

    except Exception as e:
        helper.log_errors(e)
        if counter <= 5:
            time.sleep(30)
            urls = [url]
            is_proxy = not is_proxy
            helper.log_summary((url, website_id), f"Error occured. Trying again after 30 sec. ( Tries {counter+1}).")
            urls = get_page_urls(url, website_id, urls, is_proxy, counter+1)
    return urls


def scrape_real_estate(url,log_url, website_id, is_proxy=0, counter=1):
    data = []
    proxy = None
    try:
        if is_proxy:
            proxy = {
                "https": helper.get_random_proxy()
            }
        seconds = helper.get_random_number(20, 30)
        useragent = UserAgent(use_cache_server=False)
        headers = {'User-Agent': useragent.random}
        page = requests.get(url, headers=headers, timeout=seconds, proxies=proxy)
        soup = BeautifulSoup(page.content, "html.parser")
        soup = helper.convert_codes_to_html(soup)
        real_estates_ul = soup.find(id="srchrslt-adtable")

        for item in real_estates_ul.findAll('li', class_=["lazyload-item"]):
            real_estate_object = {}
            if isinstance(item, Tag):
                try:
                    article = item.find('article')
                    try:
                        real_estate_object['url'] = base_url + article['data-href']
                    except:
                        real_estate_object['url'] = None
                    try:
                        price = item.find("p", {"class": "aditem-main--middle--price"}).contents[0].strip()
                        # price = re.findall('\d*\.?\d+', price)[0]
                        price = price.split(' ')[0]
                        price = price.replace('.', '')
                        price = price.replace(',', '')
                        price = int(price)
                        real_estate_object['price'] = price
                    except Exception as e:
                        print('price error:', e)
                        real_estate_object['price'] = None
                    try:
                        area = item.findAll("span", {"class": "simpletag tag-small"})[0].contents[0].strip()
                        # area = re.findall('\d*\.?\d+', area)[0]
                        area = area.split(' ')[0]
                        area = float(area.replace(',', '.'))
                        real_estate_object['area'] = area
                    except Exception as e:
                        print('area error:', e)
                        real_estate_object['area'] = None
                    real_estate_object['file_path'] = ""

                    data.append(real_estate_object)

                except Exception as e:
                    helper.log_errors(e)

        helper.log_summary((log_url, website_id), "Page scraped completely.")
    except Exception as e:
        helper.log_errors(e)

        if counter <= 5:
            time.sleep(30)
            urls = [url]
            is_proxy = not is_proxy
            helper.log_summary((log_url, website_id), f"Error occured. Trying again after 30 sec. ( Tries {counter+1}).")
            data = scrape_real_estate(url, log_url, website_id, is_proxy, counter+1)

    return data


def main():
    urls = []

    # print(scrape_real_estate(url))
    get_page_urls(base_url, urls, 0)
    print(len(urls))
    print(urls)


if __name__ == '__main__':
    main()
