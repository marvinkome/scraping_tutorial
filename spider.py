'''
Author:Marvin Kome
'''

import re
import random
import datetime
import csv
from urllib.request import urlopen
import pymysql
from bs4 import BeautifulSoup

INTERNAL_PAGES = set()
EXTERNAL_PAGES = set()

random.seed(datetime.datetime.now())

def main(url):
    ''' Main function to run'''
    get_random_link(url)

    print('No. internal links in site {0}'.format(len(INTERNAL_PAGES)))
    print('No. external links in site {0}'.format(len(EXTERNAL_PAGES)))
    #to_db('demo', 'internal_links', INTERNAL_PAGES)
    #to_db('demo', 'external_links', EXTERNAL_PAGES)
    to_csv(INTERNAL_PAGES, 'internal_links')
    to_csv(EXTERNAL_PAGES, 'external_links')

def add_to_set(func_set, value):
    ''' Adds an item to a set and return a boolean if it was added'''
    init_len = len(func_set)
    func_set.add(value)
    return len(func_set) != init_len

def split_url(url):
    ''' Split the url and return the site name for re'''
    url = url.replace("http://", "")
    url = url.split('/')
    url = url[0].split('.')
    length = len(url)

    if length == 3:
        return url[1]

    return url[0]

def get_internal_links(url):
    ''' Return all internal links'''
    internal_links = []
    splited_url = split_url(url)
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, 'html.parser')

    links = bs_obj.find_all('a', href=re.compile("^(/|.*"+splited_url+")"))

    for link in links:
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in internal_links:
                internal_links.append(link.attrs['href'])

    return internal_links

def get_external_links(url):
    ''' Return list of external links'''
    external_links = []
    splited_url = split_url(url)
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, 'html.parser')

    links = bs_obj.find_all("a", href=re.compile("^(http|www)((?!"+splited_url+").)*$"))

    for link in links:
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in external_links:
                external_links.append(link.attrs['href'])

    return external_links

def get_random_link(url):
    ''' Add links to global sets of internal and external link.
    Then go to another page and repeat the function recursively '''
    external_links = get_external_links(url)
    internal_links = get_internal_links(url)
    print('No. of internal link in this page {0}'.format(len(internal_links)))
    print('No. of external link in this page {0}'.format(len(external_links)))

    added_internal_links = 0
    for internal_link in internal_links:
        internal_addition = add_to_set(INTERNAL_PAGES, internal_link)
        if internal_addition:
            added_internal_links += 1

    print("Added {0} Internal Links".format(added_internal_links))

    added_external_links = 0
    for external_link in external_links:
        external_addition = add_to_set(EXTERNAL_PAGES, external_link)
        if external_addition:
            added_external_links += 1

    print("Added {0} External Links".format(added_external_links))

    print('Current Size of internal link {0}'.format(len(INTERNAL_PAGES)))
    print('Current Size of enternal link {0}'.format(len(EXTERNAL_PAGES)))
    print("-" * 10)

    # Go to a random internal link if there's a link
    length = len(internal_links)
    if length != 0:
        random_link = internal_links[random.randint(0, len(internal_links) - 1)]
    else:
        return

    # Call the function recursively
    print('Now visiting {0}'.format(random_link))
    get_random_link(random_link)

def to_csv(items, filename):
    ''' Sends a set of item to a csv file '''
    csv_file = open(filename+".csv", 'w+')
    item_list = list(items)

    try:
        writer = csv.writer(csv_file)
        writer.writerow(('id', 'link'))
        for item_id, item in enumerate(item_list):
            writer.writerow((item_id, item))

    finally:
        csv_file.close()

def to_db(db_name, row, items, user='root', pswd=None):
    ''' Sends the items to the database '''
    item_list = list(items)
    conn = pymysql.connect(host='127.0.0.1',
                           user=user, passwd=pswd, db=db_name, charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute("USE demo")
        for link in item_list:
            cur.execute('INSERT INTO links ({0}) VALUES ("{1}")'.format(row, link))
            cur.connection.commit()
            print('Content Added to database')
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    main('http://localhost/wp-1/')
