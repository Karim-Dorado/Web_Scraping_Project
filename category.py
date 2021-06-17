# -*- coding: utf-8 -*-
import argparse
import requests
from bs4 import BeautifulSoup


def scrape_cat(url):
    """
    This function makes a request from a category page of the web site
    http://books.toscrape.com/, and returns a list containing the URL
    of the Product page of each book belonging to this category.
    :param : A string containing the URL of a category page
    ex:'http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html'
    """
    url_list = []
    r = requests.get(url)
    if r.ok:
        encoding = r.encoding if "charset" in r.headers.get(
            "content-type", "").lower() else None
        soup = BeautifulSoup(r.content,
                             from_encoding=encoding,
                             features="html.parser")
        body = soup.find('body')
        li = body.find("li", {"class": "current"})
        try:
            nb_pages = int(li.text.split()[3])
            cat_list = [url[:-10] + 'page-' + str(i) + '.html'
                        for i in range(2, nb_pages + 1)]
            cat_list.insert(0, url)
        except AttributeError:
            cat_list = [url]
        for url in cat_list:
            r = requests.get(url)
            if r.ok:
                encoding = r.encoding if "charset" in r.headers.get(
                    "content-type", "").lower() else None
                soup = BeautifulSoup(r.content,
                                     from_encoding=encoding,
                                     features="html.parser")
                h3s = soup.find_all('h3')
                for h3 in h3s:
                    url_list.append(
                        "http://books.toscrape.com/catalogue" +
                        h3.a['href'][8:])
    return url_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape a Category')
    parser.add_argument('--url',
                        type=str,
                        metavar='',
                        help='URL of a category')
    args = parser.parse_args()
    print(scrape_cat(args.url))
