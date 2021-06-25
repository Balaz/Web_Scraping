"""
Reddit scraping project to analyze frequently mentioned stocks generated from posts, influencers or social media
"""
from collections import Counter
from collections import deque
from collections import defaultdict

import pandas as pd

from my_logging import logging
import web_scraper


results = defaultdict(list)


def create_csv_file(relevant_posts) -> None:
    """
    Creates a database from the scraped data from reddit
    :param relevant_posts: dictionary
    :return: None
    """
    logging.info("__Creating CSV File__")
    df = pd.DataFrame.from_dict(relevant_posts, orient="index", columns=["mentions", "posts"])
    df = df.sort_values(by=["mentions"], ascending=False, kind="mergesort")
    df.to_csv("data/worthy_stocks_on_revolut.csv")


def score_comment(comment):
    if comment.author == "VisualMod":
        return
    else:
        print(comment.body, comment.score)


def scrape_comments(all_mentioned_stocks_df) -> None:
    """
    Scraping comments of a reddit post with DFS
    :param relevant_posts: dictionary
    :return: None
    """
    logging.info("__Scraping comments of a post__")

    # TODO:
    #  - uj lista a postok komment alapjan torteno ertekeleseivel
    #  - amit hozzaadunk majd a meglevo dictionaryhoz uj oszlopkent
    #  - plusz 1 oszlop hogy vegeredmenyben pos, semleges vagy negativ az ertekeles

# --------------------------------------------
    # Checking the post from the database
    #   -> No need to scrape the website for posts every time while figuring out how to score comments
    #  we only need one stock
    relevant_posts = pd.read_csv("data/worthy_stocks_on_revolut.csv", nrows=1, usecols=["posts"])
    for index, row in relevant_posts.iterrows():
        # creating a list from a string
        list_of_posts_ids = row.values[0].strip("[]").replace("'", "").split(", ")

    #  we only need one post
    for post_id in list_of_posts_ids[:1]:
        post = reddit.submission(id=post_id)
        print(post.title)
# --------------------------------------------

        # The max depth of the comments
        post.comments.replace_more(limit=None)
        # Grabs all the top level comments
        comment_queue = deque(post.comments[:])
        while comment_queue:
            comment = comment_queue.popleft()
            score_comment(comment)
            comment_queue.extendleft(reversed(comment.replies))



def filter_rev_stocks(all_rev_stocks_df) -> pd.DataFrame:
    """
    We are care about stocks, which are mentioned in the posts
    :param wallstreetbets_hot_posts:
    :return: pd.DataFrame
    """
    wallstreetbets_hot_posts = web_scraper.scrape_wallstreetbets_posts()

    new_dict = defaultdict(list)
    for post in wallstreetbets_hot_posts:
        for stock in all_rev_stocks_df["Symbol"]:
            # I only catch uppercased stocks in posts because of these kind of stocks: A, CARS, ALL, ON etc...
            if (" " + stock + " ") in (" " + post.title + " "):
                new_dict[stock].append(post.id)

    df1 = pd.DataFrame([(k, v) for k, v in new_dict.items()], columns=["Symbol", "Post IDs"])

    all_mentioned_stocks_df = all_rev_stocks_df.merge(df1, how="inner", on="Symbol")

    all_mentioned_stocks_df.to_csv("data/mentioned_revolut_stocks.csv")

def main() -> None:
    logging.info("__Scraping reddit posts__")

    all_rev_stocks_df = web_scraper.scrape_all_stocks_from_revolut()
    all_mentioned_stocks_df = filter_rev_stocks(all_rev_stocks_df)
    # scrape_comments(all_mentioned_stocks_df)

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
    main()
    # scrape_comments()
