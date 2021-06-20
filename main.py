"""
Reddit scraping project to analyze frequently mentioned stocks
"""
import json

from my_logging import logging
import praw
import web_scraper


list_of_stocks = web_scraper.get_revolut_stocks_name()


def get_credentials():
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


def scrape_reddit():
    logging.info("__Starts scraping__")
    reddit = get_credentials()
    hot_posts = reddit.subreddit('wallstreetbets').top("day")
    for post in hot_posts:
        for stock in list_of_stocks:
            if (" " + stock + " ") in (" " + post.title + " "):
                print(post.title, stock)


    # TODO:
    #  talalatok alapjan melyik stock szerepelt hányszor
    #  összehasonlitva a topicok pontozásával
    #  nem csak a stock nevek kellenek hanem a score
    #  megnézni a kommenteket is
    #  vlmi logikát rá kitalálni


if __name__ == '__main__':
    scrape_reddit()