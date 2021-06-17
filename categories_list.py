# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def scrape_cat_list():
    """
    This function makes a request from the web site http://books.toscrape.com/,
    and returns a list of each category page belonging to this web site.
    It doesn't need any parameter.
    """
    url = 'http://books.toscrape.com'
    r = requests.get(url)
    if r.ok:
        cat_url_list = []
        encoding = r.encoding if "charset" in r.headers.get(
            "content-type", "").lower() else None
        soup = BeautifulSoup(r.content,
                             from_encoding=encoding,
                             features="html.parser")
        body = soup.find('body')
        ul = body.find("ul", {"class": "nav nav-list"})
        a_list = ul.find_all('a')
        for a in a_list[1:]:
            cat_url_list.append('http://books.toscrape.com/' + a['href'])
        return cat_url_list


if __name__ == '__main__':
    print(scrape_cat_list())
