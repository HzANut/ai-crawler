import scrapy
from collections import defaultdict, Counter
import bs4
from bs4 import BeautifulSoup
from bs4.element import Tag
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
import os

class TokenSpider(scrapy.Spider):
    name = "token_spider"

    def __init__(self, *args, **kwargs):
        super(TokenSpider, self).__init__(*args, **kwargs)
        self.token_stats = defaultdict(lambda: defaultdict(Counter))
        self.local_html = False

    def start_requests(self):

        urls = getattr(self, 'urls', None)
        if urls:
            for _url in urls.split(','):            
                yield scrapy.Request(url=_url, callback=self.parse)

    def parse(self, response):

        page = response.url.split("/")[-1]
        soup = BeautifulSoup(response.body, 'lxml')
        self.get_tokens_by_layer(soup, layer=0, stats=self.token_stats[page])
        self.print_stats(self.token_stats)

    def count_token(self, soup_element, token):
        element_text = soup_element.get_text().lower()
        return element_text.count(token.lower())

    '''
    maxlayers = 4
    '''
    def find_token_in_layers(self, element, token, token_stats, current_layer=1, max_layers=4):

        # element_copy = BeautifulSoup(str(element), 'html.parser')

        if current_layer - 1 > max_layers:
            # text_content = element.get_text()
            # count = text_content.count(token)
            # if count == 0:
            #     return
            # save layer 5th
            return 0
        # print(type(element))
        if len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag):
            # print(type(element))
            print(f'########################## element: {element} - {self.count_token(element, token)}')
            return self.count_token(element, token)
            
        curr_token_count = 0

        children = self.find_children(element)
        # print(f'children **** {children}')
        for child in children:
            child_token_count = self.find_token_in_layers(child, token, token_stats, current_layer+1)
            print(f'child token count: {child_token_count} child: {child} next layer: {current_layer + 1}')
            curr_token_count += child_token_count
        


        # for child in element.find_all():

            # print(f'tag child: {child}')
            # child_token_count = self.count_token(child, token)
            # curr_token_count -= child_token_count
            # self.find_token_in_layers(child, token, token_stats, current_layer + 1)

        # if current_layer not in token_stats:
        #     token_stats[current_layer] = 0
        token_stats[current_layer] = curr_token_count


        return curr_token_count

    def find_children(self, element):
        return [child for child in element.contents if child != '\n']

    def element_with_token(self, element, token):
        tags = element.find_all(token)
        return tags

    def count_token_in_element(self, element, token):
        tags = self.element_with_token(element, token)
        
        counts = [self.count_token(tag, token) for tag in tags]

        return sum(counts)
        

    # def get_tokens_by_layer(self, soup, layer=0, stats=None):
    #     soup_txt = soup.get_text().encode('ascii', 'ignore').decode('ascii')
    #     tokens = word_tokenize(soup_txt)
    #     stats[layer].update(tokens)

    #     for child in soup.children:
    #         if hasattr(child, 'children'):
    #             self.get_tokens_by_layer(child, layer + 1, stats)

    def print_stats(self, stats):
        for page, layers in stats.items():
            self.logger.info(f"Page: {page}")
            for layer, counter in layers.items():
                self.logger.info(f"  Layer {layer}:")
                for token, count in counter.items():
                    self.logger.info(f"    {token}: {count}")