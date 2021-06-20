from my_logging import logging

import requests
import bs4


def get_site(site_URL):
    """
    Sends a GET request to a website and checking it for exceptions
    :param str
    :return: Response Object
    """
    logging.info("__Sending the GET request for Revolut stocks's site__")

    try:
        response = requests.get(site_URL)
    except Exception as http_err:
        logging.critical(http_err)
    else:
        return response


def get_revolut_stocks_name() -> list:
    """
    Scrapes all the stocks's names used by Revolut and returns them in a list
    (Upgradeable with pandas - less code)
    :return: list
    """
    logging.info("__Scraping for the table, which contains the stocks__")

    all_revolut_stocks_site_URL = "https://globefunder.com/revolut-stocks-list/"
    site_response = get_site(all_revolut_stocks_site_URL)

    site_in_html = bs4.BeautifulSoup(site_response.content, 'html.parser')
    table = site_in_html.find("table")
    table_body = table.find("tbody")
    rows = table_body.find_all('tr')
    list_of_stocks = []
    for row in rows:
        asd = row.find_all('td')
        list_of_stocks.append(asd[2].text.strip())

    return list_of_stocks



