import unittest
from scrapy.http import Request
from html_token_analyzer.spiders.token_spider import TokenSpider
from bs4 import BeautifulSoup
from collections import defaultdict, Counter

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

    def test_count_token_phrase(self):
        token = "take over"

        html_content = """
            <a>
                <p>My content to take over</p>
                <div>
                    <span>Another content</span>
                    <div>Take over the moon</div>
                </div>
                <p>Yet another paragraph</p>
            </a>
            """

        soup = BeautifulSoup(html_content, 'html.parser')

        count = self.spider.count_token(soup, token)

        print(f'token[{token}] - count[{count}]')
        self.assertEqual(count, 2)


    def test_count_token_ignore_case(self):
        token = "a"

        html_content = """
            <a>
                <p>a</p>
                <div>
                    <span>A</span>
                    <div>Ta</div>
                </div>
                <p>AA</p>
            </a>
            """

        soup = BeautifulSoup(html_content, 'html.parser')

        count = self.spider.count_token(soup, token)

        print(f'token[{token}] - count[{count}]')
        self.assertEqual(count, 5)

    def test_find_token_in_layers(self):
        token = "a"

        token_stats = defaultdict(int)

        html_content = """
            <a>
                <p>a</p>
                <div>
                    <p>b</p>
                    <span>A</span>
                    <div>Ta</div>
                </div>
                <p>AA</p>
            </a>
            """

        soup = BeautifulSoup(html_content, 'html.parser')
        # print(f'soup.contents: {soup.contents}')
        # print('===========================================')
        # print(f'soup.contents: {soup.contents[1].contents}')
        # print('===========================================')
        # print(f'soup.contents: {soup.contents[1].contents[1].contents}')
        # print(f'soup.contents: {type(soup.contents[1].contents[1].contents[0])}')
        # print(f'soup.contents: {soup.contents[1].contents[3]}')

        self.spider.find_token_in_layers(soup, token, token_stats)

        # print(f'================= token_stats: {token_stats}')


    # def test_elements_with_token(self):
    #     token = "a"

    #     token_stats = defaultdict(int)

    #     html_content = """
    #         <a>
    #             <p>a</p>
    #             <div>
    #                 <span>A</span>
    #                 <div>Ta</div>
    #             </div>
    #             <p>AA</p>
    #         </a>
    #         """
    #     soup = BeautifulSoup(html_content, 'html.parser')

    #     count = self.spider.elements_with_token(soup, token)
        

    def test_count_token_in_element(self):
        token = "a"

        token_stats = defaultdict(int)

        # html_content = """
        #     <a>
        #         <p>a</p>
        #         <div>
        #             <span>A</span>
        #             <div>Ta</div>
        #         </div>
        #         <p>AA</p>
        #     </a>
        #     """
        html_content = """
            <div>
                <span>A</span>
                <div>Ta</div>
            </div>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        count = self.spider.count_token_in_element(soup, token)
        # print(f'count: {count}')
        self.assertIsInstance(count, int)
        self.assertEqual(count, 2)

    # def test_find_children(self):
    #     html_content = """
    #         <a>
    #             <p>a</p>
    #             <div>
    #                 <span>A</span>
    #                 <div>Ta</div>
    #             </div>
    #             <p>AA</p>
    #         </a>
    #         """
    #     soup = BeautifulSoup(html_content, 'html.parser')
    #     children = self.spider.find_children(soup)
        # print(type(children[0]))
        # print(f'children: {children}')

    # def test_count_token_in_element(self):
    #     token = "a"

    #     token_stats = defaultdict(int)

    #     html_content = """
    #         <a>
    #             <p>a</p>
    #             <div>
    #                 <span>A</span>
    #                 <div>Ta</div>
    #             </div>
    #             <p>AA</p>
    #         </a>
    #         """
    #     soup = BeautifulSoup(html_content, 'html.parser')
    #     count = self.spider.count_token_in_element(soup, token)
    #     print(f'count: {count}')

    def test_toekn_layer_stats(self):
        token = "a"

        token_stats = defaultdict(int)

        html_content = """
            <a>
                <p>a</p>
                <div>
                    <p>b</p>
                    <span>A</span>
                    <div>Ta</div>
                </div>
                <p>AA</p>
            </a>
            """

        soup = BeautifulSoup(html_content, 'html.parser')

        self.spider.token_layer_stats(soup, token, token_stats)
        print(f'================= token_stats: {token_stats}')

    def tearDown(self):
        # Code that runs after each test, often used to clean up
        pass

if __name__ == "__main__":
    unittest.main()