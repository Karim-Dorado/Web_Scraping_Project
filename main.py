# -*- coding: utf-8 -*-
import csv
import os
import requests
import time

import books
import category
import categories_list


def main():
    """
    This function makes a request from the web site http://books.toscrape.com/,
    and returns a dict of each book from each category belonging to this
    web site.
    It doesn't need any parameter.
    """
    books_scraped = {}
    categories = categories_list.scrape_cat_list()
    date = time.strftime("%d-%m-%Y-%Hh%M")
    directory = "Books_to_Scrape_" + date
    try:
        os.mkdir(os.path.join(os.getcwd(), directory))
        os.chdir(os.path.join(os.getcwd(), directory))
    except FileExistsError:
        raise Exception(f"Error : {directory} folder already exists !"
                        "\nPlease rename/delete it if you want "
                        "this utility runs correctly.")
    for categorie in categories:
        cat = category.scrape_cat(categorie)
        books_category = ''.join(
            c for c in categorie.split('/')[6] if c.isalpha()).capitalize()
        print("Collecting data from :", books_category)
        books_scraped[books_category] = []
        try:
            os.mkdir(os.path.join(os.getcwd(), books_category))
            os.chdir(os.path.join(os.getcwd(), books_category))
        except FileExistsError:
            raise Exception(f"Error :{books_category} folder already exists ! "
                            "\nPlease rename/delete it if you want "
                            "this utility runs correctly.")
        for url in cat:
            book = books.scrape_book(url)
            books_scraped[books_category].append(book)
        img_dir = "Images"
        try:
            os.mkdir(os.path.join(os.getcwd(), img_dir))
            os.chdir(os.path.join(os.getcwd(), img_dir))
        except FileExistsError:
            raise Exception(f"Error :{img_dir} folder already exists ! "
                            "\nPlease rename/delete it if you want "
                            "this utility runs correctly.")
        for b in books_scraped[books_category]:
            r = requests.get(b['image_url'])
            img_name = b['title'].translate({ord(':'): None,
                                             ord('/'): None,
                                             ord('*'): None,
                                             ord('?'): None,
                                             ord(':'): None,
                                             ord('<'): None,
                                             ord('>'): None,
                                             ord('"'): None,
                                             ord('\\'): None}) + ".jpg"
            if r.ok:
                with open(img_name, 'wb') as f:
                    f.write(r.content)
        os.chdir("..")
        filename = f'{books_category}.csv'
        with open(filename, "w", newline='', encoding='utf-8') as f:
            fieldnames = [
                'title',
                'upc',
                'price_excluding_tax',
                'price_including_tax',
                'number_available',
                'product_description',
                'review_rating',
                'category',
                'image_url'
            ]
            writer = csv.DictWriter(f,
                                    fieldnames=fieldnames,
                                    delimiter='|')
            writer.writeheader()
            for value in books_scraped[books_category]:
                writer.writerow(value)
        print("Data collected from :", books_category)
        books_scraped = {}
        os.chdir("..")


if __name__ == '__main__':
    main()
