"""
Reddit scraping project to analyze frequently mentioned stocks generated from posts, influencers or social media
"""
from collections import defaultdict
from collections import deque
import pandas as pd

from my_logging import logging
import web_scraper


def create_csv_file() -> None:
    """"""
    logging.info("__Creating CSV File__")


def score_comment(comment):
    """"""
    if comment.author == "VisualMod" or comment.author is None:
        return
    else:
        print(comment.body, comment.score)


def scrape_comments() -> None:
    """"""
    logging.info("__Scraping comments of a post__")

    # TODO:
    #  - uj lista a postok komment alapjan torteno ertekeleseivel
    #  - amit hozzaadunk majd a meglevo dictionaryhoz uj oszlopkent
    #  - plusz 1 oszlop hogy vegeredmenyben pos, semleges vagy negativ az ertekeles

    # ---------------GET POST IDS FROM DATABASE-----------------------------
    # We only need one stock from the database
    relevant_posts = pd.read_csv("data/mentioned_revolut_stocks.csv", nrows=1, usecols=["Post IDs"])
    for row, series_of_posts_ids in relevant_posts.iterrows():
        for column_name, string_of_posts_ids in series_of_posts_ids.items():
            list_of_posts_ids = list(map(str, string_of_posts_ids.strip('][').replace("'", '').split(', ')))
            for post_id in list_of_posts_ids[:1]:
                post = web_scraper.get_comments(post_id)
                print(post.title)
    # ------------------SCRAPE COMMENTS--------------------------
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
    :param all_rev_stocks_df:
    :return: pd.DataFrame
    """
    wallstreetbets_hot_posts = web_scraper.get_wallstreetbets_posts()

    new_dict = defaultdict(list)
    for post in wallstreetbets_hot_posts:
        for stock in all_rev_stocks_df["Symbol"]:
            # I only catch uppercased stocks in posts because of these kind of stocks: A, CARS, ALL, ON etc...
            if (" " + stock + " ") in (" " + post.title + " "):
                new_dict[stock].append(post.id)

    df1 = pd.DataFrame([(k, v, len(v)) for k, v in new_dict.items()], columns=["Symbol", "Post IDs", "Number of posts"])

    all_mentioned_stocks_df = all_rev_stocks_df.merge(df1, how="inner", on="Symbol", sort="ascending")
    all_mentioned_stocks_df.sort_values(by='Number of posts', ascending=False, inplace=True)
    all_mentioned_stocks_df.to_csv("data/mentioned_revolut_stocks.csv")


def main() -> None:
    logging.info("__Scraping reddit posts__")

    all_rev_stocks_df = web_scraper.get_all_stocks_from_revolut()
    all_mentioned_stocks_df = filter_rev_stocks(all_rev_stocks_df)
    scrape_comments(all_mentioned_stocks_df)

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
    #  +
    #  Egy masodik korben meg lehetne nezni azoknak a posztoknak a kommentjeit amiket kiszurtunk -
    #    - egy extra lekeres ha tobb infot szeretnenk az adott reszvenyrol

if __name__ == '__main__':
    # main()
    scrape_comments()
