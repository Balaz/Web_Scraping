"""
Reddit scraping project to analyze frequently mentioned stocks generated from posts, influencers or social media
"""
from collections import Counter
from collections import deque
from collections import defaultdict
import json
import praw
import pandas as pd

from my_logging import logging
import web_scraper


list_of_revolut_stocks = web_scraper.get_revolut_stocks_name()
results = defaultdict(list)


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


def score_comment(comment):
    print(comment.body, comment.score)


def scrape_comments(post) -> None:
    """
    Scraping comments of a reddit post with DFS
    :param post: Subreddit instance
    :return: None
    """
    logging.info("__Scraping comments of a post__")
    # The max depth of the comments
    post.comments.replace_more(limit=None)
    # Grabs all the top level comments
    comment_queue = deque(post.comments[:])
    while comment_queue:
        comment = comment_queue.popleft()
        score_comment(comment)
        comment_queue.extendleft(reversed(comment.replies))


def check_stock_names_in_posts(wallstreetbets_hot_posts) -> list():
    """
    It checks if someone mentioned a revolut stock in the title of a post and collects and returns them in a list
    :param wallstreetbets_hot_posts: list of subreddit instances
    :return: list of subreddit instances
    """
    result = defaultdict()
    result.update({"stocks": ["mentions", "posts"]})

    stock_mentioned_posts = defaultdict(list)
    mentioned_stocks_counter = Counter()

    for post in wallstreetbets_hot_posts:
        for stock in list_of_revolut_stocks:
            # I only catch uppercased stocks in posts because of these kind of stocks: A, CARS, ALL, ON etc...
            if (" " + stock + " ") in (" " + post.title + " ") or \
                    (" " + stock + " ") in ("$" + post.title + " "):
                stock_mentioned_posts[stock].append(post)
                mentioned_stocks_counter.update([stock])

    for mentioned_stock, counter in mentioned_stocks_counter.items():
        result.update({mentioned_stock: [counter, stock_mentioned_posts[mentioned_stock]]})

    return result


def scrape_reddit_posts() -> None:
    logging.info("__Scraping reddit posts__")
    reddit = get_credentials()
    wallstreetbets_hot_posts = reddit.subreddit('wallstreetbets').top("day")

    relevant_posts = check_stock_names_in_posts(wallstreetbets_hot_posts)

    df = pd.DataFrame(relevant_posts)
    df = df.transpose()
    df.to_csv("data/worthy_stocks.csv", header=None)

    """
    for post in relevant_posts:
        print(post.title)
        # scrape_comments(post)
    """
    # TODO:
    #  Ertekelni hogy egy comment vagy title az pozitiv vagy negativ
    #    - egy eredmenyt kiolvasni - troll cikk-e vagy "megbizhato" - igy maga a reszveny
    #  Osszehasonlitani a heti eredmenyekkel - max havi - a cel eszrevenni a "FOMO" reszvenyeket,
    #     amelyek hirtelen felkapottak lesznek egy cikktol vagy egy bejegyzestol
    #  napi rendszeresseggel pl 6 orankent updatelni az ertekeket
    #    - hozafuzni a regi ertekekhez - help from https://pushshift.io/
    #  lementeni az eredmenyeket csv fileokban - pandas
    #  diagramm segitesegevel abrazolni az eredmenyt (egy vagy tobb potencialis reszveny) - Matplotlib
    #  +
    #  Valos adatokkal osszehasonlitani az eredmenyt, hogy valoban erdemes-e (vlmelyik reszvenyoldal)


if __name__ == '__main__':
    scrape_reddit_posts()
