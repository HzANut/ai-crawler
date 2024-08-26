import unittest
from scrapy.http import Request
from html_token_analyzer.spiders.token_spider import TokenSpider
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
from . import test_util

class TestTokenSpider(unittest.TestCase):
    def setUp(self):
        self.spider = TokenSpider(urls="http://example.com")


    def test_count_token_ignore_case(self):
        soup = BeautifulSoup(test_util.html_content_a, 'html.parser')

        count = self.spider.count_token(soup)

        # print(f'token[{token}] - count[{count}]')
        self.assertEqual(count, 5)


    # def test_token_layer_stats_including_nested(self):
    #     token_stats = defaultdict(int)
    #     soup = BeautifulSoup(test_util.html_content_a, 'html.parser')

    #     self.spider.token_layer_stats_including_nested(soup, test_util.token_a, token_stats)
    #     self.assertDictEqual(token_stats, {3:2, 2:5, 1:5})


    def test_find_children(self):
        soup = BeautifulSoup(test_util.html_content_a, 'html.parser')
        children = self.spider.find_children(soup, set())
        # print(type(children[0]))
        # print(f'children: {children}')
        self.assertEqual(len(children), 1)


    def test_token_layer_stats(self):
        token_stats = defaultdict(int)
        soup = BeautifulSoup(test_util.html_content_a_5layers, 'html.parser')

        self.spider.token_layer_stats(soup, token_stats)
        # print(f'token_stats: {token_stats}')
        self.assertDictEqual(token_stats, {3: 3, 2: 2, 1: 0, 5: 3, 4: 0})
        
    
    def test_token_layer_stats_disconnected(self):
        token_stats = defaultdict(int)
        soup = BeautifulSoup(test_util.html_content_a_double, 'html.parser')

        self.spider.token_layer_stats(soup, token_stats)
        self.assertDictEqual(token_stats, {3:5, 2:5, 1:0})

    def test_collect_script_tags(self):
        soup = BeautifulSoup(test_util.html_content_script, 'html.parser')
        script_tags = self.spider.collect_script_tags(soup)
        # print('-------------- script tags ---------------')
        # print(script_tags)
        self.assertEqual(len(script_tags), 3)

    def tearDown(self):
        # Code that runs after each test, often used to clean up
        pass

if __name__ == "__main__":
    unittest.main()