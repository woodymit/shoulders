import ipdb
import json

import httplib
import urllib
from bs4 import BeautifulSoup
import re

SEARCH_HOST = "scholar.google.com"
SEARCH_BASE_URL = "/scholar"

RESULTS_PER_PAGE = 20


def search_string(string, limit):
    terms = string.split(' ')
    html = search_terms(terms, limit)
    return scrape_results_page(html, limit)


def search_terms(terms, limit):
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


def get_citers_page_html(paper):
    url_suffix = paper.citers_page_href

    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    conn = httplib.HTTPConnection(SEARCH_HOST)
    conn.request("GET", url_suffix, '', headers)

    resp = conn.getresponse()

    if not resp.status == 200:
        raise Exception('Response from Google Scholar url:' +
                url_suffix + ' did not return with code 200')

    html = resp.read()
    return html.decode('ascii', 'ignore')


class Paper:
    def __init__(self, title, title_href, author_list, citers_page_href):
        self.title = title
        self.title_href = title_href
        self.author_list = author_list
        self.citers_page_href = citers_page_href

    def __hash__(self):
        return hash(self.title_href)

    # def json_repr(self):
    #     return json.dumps({
    #         'title:': self.title,
    #         'title_href:': self.title_href,
    #         'author_list:': self.author_list,
    #         'citers_page_href:': self.citers_page_href
    #         })

    def get_data_dict(self):
        return {
            'title:': self.title,
            'title_href:': self.title_href,
            'author_list:': self.author_list,
            'citers_page_href:': self.citers_page_href
            }


class CitationGraph:
    def __init__(self, center_paper):
        self.children = {center_paper: []}
        self.center = center_paper
        self.newest_edge = set([center_paper])
        self.oldest_edge = [center_paper]

    def expand_newest_edge(self, iterations=1):
        next_edge = set()
        for parent in self.newest_edge:
            child_list = get_citing_papers(parent)
            self.children[parent] = child_list
            for child in child_list:
                if child not in self.newest_edge:
                    next_edge.add(child)


def parse_result(result_tag):
    h3_tag = result_tag.find_next('h3')
    title = h3_tag.get_text()

    title_a_tag = h3_tag.find_next('a')
    if title_a_tag:
        title_href = title_a_tag.get('href')
    else:
        title_href = None

    citers_page_href = None
    for a_tag in result_tag.find_all('a'):
        if re.match('Cited by [\d]+', a_tag.get_text()):
            citers_page_href = a_tag.get('href')
            break

    author_list = []
    authors_tag = result_tag.find_next(class_='gs_a')
    for author_html in str(authors_tag).split(','):
        author_soup = BeautifulSoup(author_html)
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

    return Paper(title, title_href, author_list, citers_page_href)


def get_html(rel_url):

    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    conn = httplib.HTTPConnection(SEARCH_HOST)
    conn.request('GET', rel_url, '', headers)

    resp = conn.getresponse()

    if not resp.status == 200:
        raise Exception('Response from Google Scholar url:' +
                rel_url + ' did not return with code 200')

    html = resp.read()
    return html.decode('ascii', 'ignore')


def scrape_single_results_page(html, limit=20):

    paper_list = []
    soup = BeautifulSoup(html)
    for result_tag in soup.find_all(class_='gs_ri')[:limit]:
        paper_list.append(parse_result(result_tag))

    return paper_list


def scrape_results_page(html, limit=20):

    paper_list = scrape_single_results_page(html, limit)
    remaining = limit - RESULTS_PER_PAGE

    if remaining < 0:
        return paper_list

    soup = BeautifulSoup(html)
    next_page_url = soup.body.find('div', id='gs_top'
        ).find('div', id='gs_bdy').find('div', id='gs_res_bdy'
        ).find('div', id='gs_ccl').find('div', id='gs_n'
        ).find('a').get('href')

    next_page_html = get_html(next_page_url)

    return paper_list + scrape_results_page(
            next_page_html, remaining)


def get_citing_papers(parent_paper):

    assert parent_paper.citers_page_href
    html = get_citers_page_html(parent_paper)
    paper_list = scrape_results_page(html, 100)

    return paper_list
