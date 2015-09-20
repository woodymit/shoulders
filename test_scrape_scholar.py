from scrape_scholar import CitationGraph
from scrape_scholar import get_citers_page_html
from scrape_scholar import search_terms
from scrape_scholar import scrape_results_page
import ipdb

if __name__ == '__main__':
    # Test 1
    terms = ['Genomically', 'recoded', 'organisms']
    limit = 50
    html = search_terms(terms, limit)
    paper_list = scrape_results_page(html, limit)
    assert len(paper_list) == limit
    print len(paper_list)
    assert paper_list[0].author_list[0] != None

    # Test 2
    citers_page_html = get_citers_page_html(paper_list[0])
    assert citers_page_html

    # Test 4
    recoli_paper = paper_list[0]
    graph = CitationGraph(recoli_paper)
    graph.expand_newest_edge()
    assert len(graph.children[recoli_paper]) == 100
