import argparse

from scraper import get_articles
from embedding import encode
from utils import list_to_dict, read_all_sqlite_database, create_sqlite_talbe
from search import insert


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--url", type=str, default="https://www.ithome.com.tw/latest", help="url to scape")
    parser.add_argument("--amount", type=int, default=30, help="The maximum number of news.")

    args = parser.parse_args()

    # scraping news
    articles = get_articles(args.url, args.amount, 0)

    # encode news to embedding
    embeds = encode(articles)

    # convert embedding list to dict
    sentences_dict = list_to_dict(articles, embeds)

    # create database and table. 
    # if you aleardy create it, you can skip this.
    create_sqlite_talbe()

    # insert news and embeddings in database
    insert(sentences_dict)

    # display data in database
    datas = read_all_sqlite_database()

    for data in datas:
        print(data)