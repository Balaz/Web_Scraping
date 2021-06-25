from my_logging import logging

import requests
import praw
import json
import pandas as pd


def get_site(site_URL) -> requests.Response:
    """
    Sends a GET request to a website and checking it for exceptions
    :param site_URL: str
    :return: Response Object
    """
    logging.info("__Sending the GET request for Revolut stocks's site__")

    try:
        response = requests.get(site_URL)
    except Exception as http_err:
        logging.critical(http_err)
    else:
        return response


def scrape_all_stocks_from_revolut() -> pd.DataFrame:
    """
    Scrapes all the stocks's names used by Revolut from globefunder.com
    and returns with a dataframe
    :return: pd.DataFrame
    """
    logging.info("__Scraping for the table, which contains the stocks__")

    all_revolut_stocks_site_URL = "https://globefunder.com/revolut-stocks-list/"
    site_response = get_site(all_revolut_stocks_site_URL)

    df = pd.read_html(site_response.text)[0]
    df = df.reindex(columns=["Symbol", "Company name"])
    df.to_csv("data/all_revolut_stocks.csv")
    return df


def get_credentials() -> praw.Reddit:
    """
    Creates a Reddit scraper and checks all the credentials for it.
    :return: Reddit instance
    """
    logging.info("__Getting the Reddit credentials__")
    try:
        with open('reddit_credentials.json') as credentials:
            reddit_app_info = json.load(credentials)["reddit_app_info"]
    except FileExistsError as er:
        logging.critical(er)

    return praw.Reddit(client_id=reddit_app_info['client_id'], client_secret=reddit_app_info['client_secret'],
                       user_agent=reddit_app_info['user_agent'])


def scrape_wallstreetbets_posts():
    reddit = get_credentials()
    return reddit.subreddit('wallstreetbets').top("day")

