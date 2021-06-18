"""
Reddit scraping project to analyze frequently mentioned stocks
"""
import logging
import json

import praw

logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='[ %(levelname)-8s ] %(asctime)s - %(filename)-20s ' +
                           '{ %(funcName)23s(): %(lineno)-3s >> %(message)s',
                    datefmt='%H:%M:%S')


def get_credentials():
    logging.info("__Getting the credentials__")
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
    hot_posts = reddit.subreddit('wallstreetbets').hot(limit=10)
    for post in hot_posts:
        print("-" + post.title)



if __name__ == '__main__':
    scrape_reddit()
