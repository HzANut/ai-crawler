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


    def __init__(self, urls=None, token=None, *args, **kwargs):
        super(TokenSpider, self).__init__(*args, **kwargs)
        self.urls = urls
        self.token = token
        self.token_stats = defaultdict(int)


    def start_requests(self):          
            yield scrapy.Request(url=self.urls, callback=self.parse)

    def decoding_response(self, response):
        try:
            html_content = response.body.decode('utf-8').encode('utf-8','replace')
        except UnicodeDecodeError:
            try:
                html_content = response.body.decode('latin-1')  # Try another encoding
            except UnicodeDecodeError:
                html_content = response.body.decode('ascii', errors='ignore')
        return html_content

    def parse(self, response):
        try:
            # print(response.body)
            soup = BeautifulSoup(self.decoding_response(response), 'lxml')
            # print(f'soup:{soup.get_text()}')
            self.token_layer_stats(soup.body, self.token, self.token_stats, current_layer=1, max_layers=100)
            self.print_stats(self.token_stats)
        except Exception as ex:
            # pass
            print(f'Error when doing token layer stats on element and token {self.token}:', ex)


    def count_token(self, soup_element, token):
        element_text = soup_element.get_text().lower()
        return element_text.count(token.lower())


    def token_layer_stats_including_nested(self, element, token, token_stats, current_layer=1, max_layers=4):
        if current_layer - 1 > max_layers:
            return self.count_token(element, token)

        if len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag):
            return self.count_token(element, token)
            
        curr_token_count = 0

        children = self.find_children(element)
        for child in children:
            child_token_count = self.token_layer_stats_including_nested(child, token, token_stats, current_layer+1)
            if child_token_count != 0:
                print(f'Found token - child token count: {child_token_count} child: {child} curr layer: {current_layer}')
            curr_token_count += child_token_count

        token_stats[current_layer] = curr_token_count

        return curr_token_count

    def find_children(self, element):
        children = []
        for child in element.contents:
            if isinstance(child, bs4.element.Doctype) or isinstance(child, bs4.element.Comment) \
                or isinstance(child, bs4.element.NavigableString):
                continue
            if child != '\n':
                children.append(child)
        return children


    def token_layer_stats(self, element, token, token_stats, current_layer = 1, max_layers = 4):
       
        if current_layer - 1 > max_layers:
            # return 0
            return self.count_token(element, token)

        if self.is_bottom(element):
            return self.count_token(element, token)
            
        curr_token_count = 0

        children = self.find_children(element)
        for child in children:
            child_token_count = self.token_layer_stats(child, token, token_stats, current_layer+1, max_layers)
            if self.is_bottom(child):
                curr_token_count += child_token_count

        token_stats[current_layer] = curr_token_count

        return curr_token_count


    def is_bottom(self, element):
        return len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag)


    def print_stats(self, stats):
        print('------------------ stats -------------------')
        print(f"{stats}")