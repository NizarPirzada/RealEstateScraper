import requests
import time
from bs4 import BeautifulSoup
from bs4 import Tag
from selenium import webdriver
from utils import helper
from fake_useragent import UserAgent
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import datetime

seconds = 20
base_url = 'https://www.immowelt.de'


def get_page_urls(url, website_id, urls=[], is_proxy=0, counter=1):
    urls = []
    # urls.append(url)
    try:
        proxy = ''
        if is_proxy:
            proxy = helper.get_random_proxy()
        opts = webdriver.ChromeOptions()
        useragent = UserAgent(use_cache_server=False)
        opts.add_argument(f'user-agent={useragent.random}')
        opts.add_argument('--headless')
        # opts.add_argument()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_argument('--proxy-server=%s' % proxy)
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=opts)
        driver.get(url)
        seconds = helper.get_random_number(5, 20)
        time.sleep(seconds)

        pages = driver.find_elements_by_xpath('//*[@class="Pagination-190de"]/div/button/span')

        # iter_no = 1
        length = int(pages[-1].get_attribute('innerHTML'))
        # length = length if iter_no == 0 else 3
        for x in range(1, length):
            if '&sp=' in url:
                temp_url = url[:-1] + str(x + 1)
            else:
                temp_url = url + '&sp=' + str(x + 1)
            urls.append(temp_url)
        driver.close()
    except Exception as e:
        helper.log_errors(e)
        try:
            driver.quit()
        except:
            pass
        if counter <= 5:
            time.sleep(15)
            urls = [url]
            is_proxy = not is_proxy
            helper.log_summary((url, website_id), f"Error occured. Trying again after 15 sec. ( {counter+1}) Tries.")
            urls = get_page_urls(url, website_id, urls,  is_proxy, counter+1)
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

        time.sleep(seconds)
        useragent = UserAgent(use_cache_server=False)
        headers = {'User-Agent': useragent.random}

        page = requests.get(url, headers=headers, timeout=seconds, proxies=proxy)

        soup = BeautifulSoup(page.content, "html.parser")
        soup = helper.convert_codes_to_html(soup)
        real_estates_list = soup.find("div", class_="SearchList-22b2e")

        for item in real_estates_list.find_all("div", class_='EstateItem-1c115'):
            real_estate_object = {}
            if isinstance(item, Tag):
                article = item.find('a')
                try:
                    real_estate_object['url'] = article['href']
                except:
                    real_estate_object['url'] = None
                try:
                    price = article.find("div", {"data-test": "price"}).contents[0].strip()
                    price = price.split(' ')[0]
                    price = price.replace('.', '')
                    price = price.replace(',', '.')
                    price = float(price)
                    real_estate_object['price'] = price
                except Exception as e:
                    print('price error:', e)
                    real_estate_object['price'] = None
                try:
                    area = article.find("div", {"data-test": "area"}).contents[0].strip()
                    area = area.split(' ')[0]
                    area = float(area.replace(',', '.'))
                    real_estate_object['area'] = area
                except Exception as e:
                    print('area error:', e)
                    real_estate_object['area'] = None
                real_estate_object['file_path'] = ""

                data.append(real_estate_object)

        for item in real_estates_list.find_all("div", class_='ProjectItem-0a128'):
            if isinstance(item, Tag):

                try:
                    for article in item.find_all('a'):
                        real_estate_object = {}
                        try:
                            real_estate_object['url'] = article['href']
                        except:
                            real_estate_object['url'] = None
                        try:
                            price = article.find("div", {"data-test": "price"}).contents[0].strip()
                            price = price.split(' ')[0]
                            price = price.replace('.', '')
                            price = price.replace(',', '.')
                            price = float(price)
                            real_estate_object['price'] = price
                        except Exception as e:
                            try:
                                price = article.find("div", {"data-test": "price"})
                                price = price.contents[0].contents[0].strip()
                                price = price.split(' ')[0]
                                price = price.replace('.', '')
                                price = price.replace(',', '.')
                                price = float(price)
                                real_estate_object['price'] = price
                            except:
                                print('price error:', e)
                                real_estate_object['price'] = None
                        try:
                            area = article.find("div", {"data-test": "area"}).contents[0].strip()
                            # area = re.findall('\d*\.?\d+', area)[0]
                            area = area.split(' ')[0]
                            area = float(area.replace(',', '.'))
                            real_estate_object['area'] = area
                        except Exception as e:
                            try:
                                area = article.find("div", {"data-test": "area"})
                                area = area.contents[0].contents[0].strip()
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
            time.sleep(15)
            is_proxy = not is_proxy
            helper.log_summary((log_url, website_id), f"Error occured. Trying again after 15 sec. ( {counter+1}) Tries.")
            data = scrape_real_estate(url,log_url, website_id, is_proxy, counter+1)
    return data


def main():
    # url = 'https://www.immowelt.de/liste/essen-altendorf/wohnungen/kaufen?d=true&r=3&sd=DESC&sf=RELEVANCE'
    url = 'https://www.immowelt.de/liste/berlin/wohnungen/kaufen?sort=relevanz'
    # print(scrape_real_estate(url))
    print(get_page_urls(url, 0))

    # print(results)


if __name__ == '__main__':
    main()
