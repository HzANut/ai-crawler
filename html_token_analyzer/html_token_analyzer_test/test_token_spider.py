import unittest
from scrapy.http import Request
from html_token_analyzer.spiders.token_spider import TokenSpider
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
from . import test_util

class TestTokenSpider(unittest.TestCase):
    def setUp(self):
        self.spider = TokenSpider(urls="http://example.com, http://example.org")


    def test_start_requests(self):
        generated_requests = list(self.spider.start_requests())

        # Check the number of requests
        self.assertEqual(len(generated_requests), 2)

        # Verify that the requests are correct
        self.assertIsInstance(generated_requests[0], Request)
        self.assertEqual(generated_requests[0].url, "http://example.com")
        self.assertEqual(generated_requests[1].url, "http://example.org")


    def test_count_token_ignore_case(self):
        soup = BeautifulSoup(test_util.html_content_a, 'html.parser')

        count = self.spider.count_token(soup, test_util.token_a)

        # print(f'token[{token}] - count[{count}]')
        self.assertEqual(count, 5)


    def test_token_layer_stats_including_nested(self):
        token_stats = defaultdict(int)
        soup = BeautifulSoup(test_util.html_content_a, 'html.parser')

        self.spider.token_layer_stats_including_nested(soup, test_util.token_a, token_stats)
        self.assertDictEqual(token_stats, {3:2, 2:5, 1:5})


    def test_find_children(self):
        soup = BeautifulSoup(test_util.html_content_a, 'html.parser')
        children = self.spider.find_children(soup)
        # print(type(children[0]))
        # print(f'children: {children}')
        self.assertEqual(len(children), 1)


    def test_toekn_layer_stats(self):
        token_stats = defaultdict(int)
        soup = BeautifulSoup(test_util.html_content_a, 'html.parser')

        self.spider.token_layer_stats(soup, test_util.token_a, token_stats)
        # print(f'token_stats: {token_stats}')
        self.assertDictEqual(token_stats, {3: 2, 2: 3, 1: 0})


    def tearDown(self):
        # Code that runs after each test, often used to clean up
        pass

if __name__ == "__main__":
    unittest.main()