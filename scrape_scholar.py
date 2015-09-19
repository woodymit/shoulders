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


def search_terms(html):

    soup = BeautifulSoup(html)

    d = []
    for result_tag in soup.find_all(class_='gs_ri'):
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

        d.append((title, title_href, cited_by_href))

    return d


if __name__ == '__main__':
    terms = ['Genomically', 'recoded', 'organisms']
    limit = 20
    html = get_html(terms, limit)
    d = search_terms(html)
    print d
