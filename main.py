"""
Reddit scraping project to analyze frequently mentioned stocks generated from posts, influencers or social media
"""
from collections import defaultdict
from collections import deque
import pandas as pd

from my_logging import logging
import web_scraper
import sentiment_analysis


def create_csv_file() -> None:
    """"""
    logging.info("__Creating CSV File__")


def score_comment(comment):
    """"""
    if comment.author == "VisualMod" or comment.author is None:
        return 0.0
    else:
        score = sentiment_analysis.analyzing_comment(comment)
        return score

def scrape_comments(mentioned_revolut_stocks_df) -> None:
    """"""
    logging.info("__Scraping comments of a post__")

    # TODO:
    #  - uj lista a postok komment alapjan torteno ertekeleseivel
    #  - amit hozzaadunk majd a meglevo .csv-hez uj oszlopkent
    #  - plusz 1 oszlop hogy vegeredmenyben pos, semleges vagy negativ az ertekeles

    # ---------------GET POST IDS FROM DATABASE-----------------------------

    asd = dict({"Sentiment Analysis": []})
    #  Only first row .values[0]
    for stock in range(len(mentioned_revolut_stocks_df["Post IDs"])):
        popularity_per_stock = []
        for post_id in mentioned_revolut_stocks_df["Post IDs"][stock]:
            post = web_scraper.get_comments(post_id)
            print(post.title)
        # ------------------SCRAPE COMMENTS--------------------------
            # The max depth of the comments
            post.comments.replace_more(limit=None)
            # Grabs all the top level comments
            comment_queue = deque(post.comments[:])
            popularity_per_comment = []
            while comment_queue:
                comment = comment_queue.popleft()
                popularity_per_comment.append(score_comment(comment))
                comment_queue.extendleft(reversed(comment.replies))

            #  Popularity per post
            avg_per_post = sum(popularity_per_comment) / len(popularity_per_comment)
            if avg_per_post > 0.1:
                print("Average popularity", avg_per_post)
            popularity_per_stock.append(avg_per_post)
        avg_per_stock = sum(popularity_per_stock) / len(popularity_per_stock)


def get_mentioned_revolut_stocks(all_rev_stocks_df) -> pd.DataFrame:
    """
    We are care about stocks, which are mentioned in the posts
    :param all_rev_stocks_df:
    :return: pd.DataFrame
    """
    wallstreetbets_hot_posts = web_scraper.get_wallstreetbets_posts()

    new_dict = defaultdict(list)
    for post in wallstreetbets_hot_posts:
        for stock in all_rev_stocks_df["Symbol"]:
            # TODO:
            #  a solution for these stock: A, CARS, ALL, ON etc...
            #  Add regular expressions
            if (" " + stock + " ") in (" " + post.title + " ") or ("$" + stock + " ") in (" " + post.title + " "):
                new_dict[stock].append(post.id)

    df1 = pd.DataFrame([(k, v, len(v)) for k, v in new_dict.items()], columns=["Symbol", "Post IDs", "Number of posts"])

    mentioned_revolut_stocks_df = all_rev_stocks_df.merge(df1, how="inner", on=["Symbol"], sort="ascending")
    mentioned_revolut_stocks_df.sort_values(by='Number of posts', ascending=False, inplace=True)
    mentioned_revolut_stocks_df.to_csv("data/mentioned_revolut_stocks.csv")

    return mentioned_revolut_stocks_df

def main() -> None:
    logging.info("__Scraping reddit posts__")

    revolut_stocks_df = web_scraper.get_all_stocks_from_revolut()
    mentioned_revolut_stocks_df = get_mentioned_revolut_stocks(revolut_stocks_df)
    scrape_comments(mentioned_revolut_stocks_df)

    # TODO:

    #  Osszehasonlitani a heti eredmenyekkel - max havi - a cel eszrevenni a "FOMO" reszvenyeket,
    #     amelyek hirtelen felkapottak lesznek egy cikktol vagy egy bejegyzestol
    #  napi rendszeresseggel pl 6 orankent updatelni az ertekeket
    #    - hozafuzni a regi ertekekhez - help from https://pushshift.io/
    #  lementeni az eredmenyeket csv fileokban - pandas
    #  diagramm segitesegevel abrazolni az eredmenyt (egy vagy tobb potencialis reszveny) - Matplotlib
    #  +
    #  Valos adatokkal osszehasonlitani az eredmenyt, hogy valoban erdemes-e (vlmelyik reszvenyoldal)
    #  +
    #  Egy masodik korben meg lehetne nezni azoknak a posztoknak a kommentjeit amiket kiszürtünk -
    #    - egy extra lekeres ha tobb infot szeretnenk az adott reszvenyrol

if __name__ == '__main__':
    main()
