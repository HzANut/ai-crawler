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


    def find_token_in_layers(self, element, token, token_stats, current_layer=1, max_layers=4):

        if current_layer - 1 > max_layers:
            return 0

        if len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag):
            return self.count_token(element, token)
            
        curr_token_count = 0

        children = self.find_children(element)
        for child in children:
            child_token_count = self.find_token_in_layers(child, token, token_stats, current_layer+1)
            # print(f'child token count: {child_token_count} child: {child} next layer: {current_layer + 1}')
            curr_token_count += child_token_count

        token_stats[current_layer] = curr_token_count

        return curr_token_count

    def find_children(self, element):
        return [child for child in element.contents if child != '\n']


    def token_layer_stats(self, element, token, token_stats, current_layer = 1, max_layers = 4):

        if current_layer - 1 > max_layers:
            return 0
        
        if self.is_bottom(element):
            return self.count_token(element, token)
            
        curr_token_count = 0

        children = self.find_children(element)
        for child in children:
            child_token_count = self.token_layer_stats(child, token, token_stats, current_layer+1)
            if self.is_bottom(child):
                curr_token_count += child_token_count

        token_stats[current_layer] = curr_token_count

        return curr_token_count


    def is_bottom(self, element):
        return len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag)


    def print_stats(self, stats):
        for page, layers in stats.items():
            self.logger.info(f"Page: {page}")
            for layer, counter in layers.items():
                self.logger.info(f"  Layer {layer}:")
                for token, count in counter.items():
                    self.logger.info(f"    {token}: {count}")