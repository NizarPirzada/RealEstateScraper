import json
from WebScraping import ebay, immowelt, immoscout24
from utils.supported_websites import SupportedWebsite
from utils import helper
import traceback
import uuid

scrapper_dic = {
        SupportedWebsite.Ebay: {
            "get_pages_url": ebay.get_page_urls,
            "scrape_real_estate": ebay.scrape_real_estate
        },
        SupportedWebsite.Immowelt: {
            "get_pages_url": immowelt.get_page_urls,
            "scrape_real_estate": immowelt.scrape_real_estate
        },
        SupportedWebsite.ImmoScout24: {
            "get_pages_url": immoscout24.get_page_urls,
            "scrape_real_estate": immoscout24.scrape_real_estate
        }

    }


def main(data): #url, supported_website_id, iter_no, is_proxy=0):
    data_returned = []
    try:

        website_id = data['website_id']
        desired_price = float(data['desired_price'])
        emails = data['emails']

        supported_website_id = data['supported_website_id']
        url = data['url']
        iter_no = data['iter_no']
        is_proxy = data['is_proxy']

        urls = [url]
        if iter_no == 0:
            urls = urls + scrapper_dic[supported_website_id]['get_pages_url'](url,website_id, urls, is_proxy, )

        urls = list(dict.fromkeys(urls))
        print('No. of Pages:', len(urls))
        print(urls)
        helper.log_summary((data['url'], website_id), f"List of urls to scrape:{urls}")
        for url in urls:
            print(f"Processing url: {url}")
            helper.log_summary((data['url'], website_id), f"Processing url: {url}")
            result = scrapper_dic[supported_website_id]['scrape_real_estate'](url,data['url'],website_id, is_proxy)
            msg = "Website_Id: " + str(website_id) + ", URL: " + url + " Total Ads:  " + str(len(result)) + "\n"
            msg += json.dumps(result, indent=4)
            helper.log_writer(log_msg=msg)
            # helper.log_summary((data['url'], website_id), msg)
            helper.process_advertisements(data['url'], url, result, website_id, desired_price, emails)
            data_returned += result

            if len(result) < 5:
                # email_id = str(uuid.uuid4())[:8]
                # html = """\
                #         <html>
                #         <body>
                #             <h4>
                #             No data while scraping webpage
                #             </h4>
                #             <p>
                #             Website Id : %s
                #             </p>
                #             <p>
                #             URL : %s
                #             </p>
                #             <p>
                #             Process Id: %s
                #             </p>
                #         </body>
                #         </html>
                # """ % (str(website_id), url, email_id)
                #
                # email_data = {
                #     'emails': emails,
                #     'subject': f"Alert - No Data while Scraping Webpage.",
                #     'html': html
                # }
                helper.log_summary((data['url'], website_id), f"No Data found wile scraping website: Website Id:{str(website_id)} URL:{url}")
                # is_success, error = helper.send_gmail(email_data)
                # try:
                #     if is_success:
                #         log_summary((url, website_id), f"Email Sent. Process Id:{email_id}")
                # except:
                #     pass
        return data_returned
    except Exception as e:
        helper.log_errors(e)

if __name__ == '__main__':
    main("url", 1)
