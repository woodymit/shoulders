from scrape_scholar import get_html
from scrape_scholar import scrape_results_page
import ipdb

if __name__ == '__main__':
    terms = ['Genomically', 'recoded', 'organisms']
    limit = 20
    html = get_html(terms, limit)
    paper_list = scrape_results_page(html)
    ipdb.set_trace()
    assert paper_list[0].author_list[0] != None
    print paper_list
