import requests

from typing import List
from bs4 import BeautifulSoup


def get_articles(url: str = "https://www.ithome.com.tw/latest", amount: int = 30, page: int = 0) -> List[str]:
    # 發送HTTP請求
    response = requests.get(url)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 假設每篇文章的連結都在class為"article-link"的<a>標籤內
    # 這裡的選擇器需要根據實際網頁結構調整
    p_tags = soup.find_all('p', class_='title')

    articles = []
    
    for p_tag in p_tags:
        amount -= 1

        if amount >= 0:
            article = p_tag.find('a')

            title = article.text.strip()  # 獲取文章標題
            link = article['href']  # 獲取文章連結

            if "news" in link:
                articles.append(title)
                print(f"{amount} - Title: {title}, Link: {link}")

    if amount >= 0:
        new_articles = get_articles(f"https://www.ithome.com.tw/latest?page={page+1}", amount, page+1)
        articles = articles + new_articles

    return articles


if __name__ == "__main__":
    # 調用函數，這裡的URL需要替換成實際的文章列表頁面URL
    articles = get_articles()
    print(articles)
    print(len(articles))