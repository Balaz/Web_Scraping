"""
Reddit scraping project to analyze frequently mentioned stocks
"""
import json
from collections import Counter
from collections import deque

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

def scrape_comments(post):
    # The max depth of the comments
    post.comments.replace_more(limit=None)
    # Grabs all the top level comments
    comment_queue = deque(post.comments[:1])
    while comment_queue:
        comment = comment_queue.popleft()
        print(comment.body, comment.score)
        comment_queue.extendleft(reversed(comment.replies))

def scrape_reddit():
    logging.info("__Starts scraping__")
    reddit = get_credentials()
    wallstreetbets_hot_posts = reddit.subreddit('wallstreetbets').top("day", limit=1)
    for post in wallstreetbets_hot_posts:
        scrape_comments(post)



    """
    mentioned_stocks = Counter()
    for post in wallstreetbets_hot_posts:
        for stock in list_of_stocks:
            # TODO: upgrade regex - nicer and should check lowercase
            if (" " + stock + " ") in (" " + post.title + " ") or ("$" + stock + " ") in (" " + post.title + " "):
                mentioned_stocks.update([stock])

    print(mentioned_stocks)
    """
    # TODO:
    #  összehasonlitva a topicok pontozásával
    #  vlmi logikát rá kitalálni


if __name__ == '__main__':
    scrape_reddit()
