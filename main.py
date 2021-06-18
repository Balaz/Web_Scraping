"""
Web Scraping practice with Beautiful Soup
"""
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='Debug.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='[ %(levelname)-8s ] %(asctime)s - %(filename)-20s ' +
                           '{ %(funcName)23s(): %(lineno)-3s >> %(message)s',
                    datefmt='%H:%M:%S')

def get_request(page_url:str) -> str:
    """
    Requesting an HTML page and checking the response from the server
    :param page_url: str
    :return: str
    """
    logging.info("___Requesting the site___")
    try:
        page_sourced = requests.get(page_url).content
    except Exception as http_err:
        logging.critical(http_err)
    else:
        return page_sourced


def main():
    page_url = "https://www.wholefoodsmarket.com/sales-flyer?store-id=10005"
    page_sourced = get_request(page_url)
    html_content = BeautifulSoup(page_sourced, "html.parser")

    sale_items = html_content.findAll('h4', class_="w-sales-tile__product")
    sale_item_titles = [i.text for i in sale_items]
    print(sale_item_titles)



if __name__ == '__main__':
    main()


