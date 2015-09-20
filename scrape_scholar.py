import ipdb

import httplib
import urllib
from bs4 import BeautifulSoup
import re

SEARCH_HOST = "scholar.google.com"
SEARCH_BASE_URL = "/scholar"


def get_html(terms, limit):
    params = urllib.urlencode({'q': "+".join(terms), 'num': limit})
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    url = SEARCH_BASE_URL+"?"+params
    conn = httplib.HTTPConnection(SEARCH_HOST)
    conn.request("GET", url, '', headers)

    resp = conn.getresponse()

    if not resp.status == 200:
        raise Exception('Response from Google Scholar url:' +
                url + ' did not return with code 200')

    html = resp.read()
    return html.decode('ascii', 'ignore')


class Paper:
    def __init__(self, title, title_href, author_list, cited_by_href):
        self.title = title
        self.title_href = title_href
        self.author_list = author_list
        self.cited_by_href = cited_by_href


def parse_result(result_tag):
    h3_tag = result_tag.find_next('h3')
    title = h3_tag.get_text()

    title_a_tag = h3_tag.find_next('a')
    if title_a_tag:
        title_href = title_a_tag.get('href')
    else:
        title_href = None

    cited_by_href = None
    for a_tag in result_tag.find_all('a'):
        if re.match('Cited by [\d]+', a_tag.get_text()):
            cited_by_href = a_tag.get('href')
            break

    author_list = []
    authors_tag = result_tag.find_next(class_='gs_a')
    for author_html in str(authors_tag).split(','):
        author_soup = BeautifulSoup(author_html)
        # ipdb.set_trace()
        author_link_list = author_soup.find_all('a')
        if author_link_list:
            author_href = author_link_list[0].get('href')
        else:
            author_href = None
        author_name = author_soup.get_text()

        ellipsis_index = author_name.find(u'\xe2\x80\xa6')
        if ellipsis_index != -1:
            author_name = author_name[:ellipsis_index]
            author_list.append((author_name, author_href))
            break

        author_list.append((author_name, author_href))

    return Paper(title, title_href, author_list, cited_by_href)


def scrape_results_page(html):

    paper_list = []
    soup = BeautifulSoup(html)
    for result_tag in soup.find_all(class_='gs_ri'):
        paper_list.append(parse_result(result_tag))

    return paper_list


# def get_cited_papers(parent_paper):

#     assert parent_paper.cited_by_href
