import scrapy
from collections import defaultdict, Counter
import bs4
from bs4 import BeautifulSoup
from bs4.element import Tag
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
import re

class TokenSpider(scrapy.Spider):
    name = "token_spider"


    def __init__(self, urls=None, testing=None, *args, **kwargs):
        super(TokenSpider, self).__init__(*args, **kwargs)
        self.urls = urls
        self.testing = True if testing else False
        self.occurance_contents = ""
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
            soup = BeautifulSoup(self.decoding_response(response), 'lxml')

            # self.write_occurrences(soup.body, self.token)

            self.token_layer_stats(soup.body, self.token, self.token_stats, current_layer=1, max_layers=100)
            self.print_stats(self.token_stats)
            
        except Exception as ex:
            print(f'Error when doing token layer stats on element and token {self.token}:', ex)


    def count_token(self, soup_element):
        word_count = len(re.findall(r'\b\w+\b', soup_element.get_text()))
        return word_count



    # def token_layer_stats_including_nested(self, element, token, token_stats, current_layer=1, max_layers=4):
    #     if current_layer - 1 > max_layers:
    #         return self.count_token(element, token)

    #     if len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag):
    #         return self.count_token(element, token)
            
    #     curr_token_count = 0

    #     children = self.find_children(element)
    #     for child in children:
    #         child_token_count = self.token_layer_stats_including_nested(child, token, token_stats, current_layer+1)
    #         curr_token_count += child_token_count

    #     token_stats[current_layer] = curr_token_count

    #     return curr_token_count
    

    def find_children(self, element, script_tags_set):
        children = []
        for child in element.contents:
            if isinstance(child, bs4.element.Doctype) or isinstance(child, bs4.element.Comment) \
                or isinstance(child, bs4.element.NavigableString) or child in script_tags_set:
                continue
            if child != '\n':
                children.append(child)
        return children


    def token_layer_stats(self, element, token_stats, current_layer = 1, max_layers = 4):
       
        if current_layer > max_layers:
            token_stats[current_layer] += self.count_token(element)
            return 0

        if self.is_bottom(element):
            return self.count_token(element)
            
        script_tags_set = set(self.collect_script_tags(element))

        curr_token_count = 0

        children = self.find_children(element, script_tags_set)
        for child in children:
            child_token_count = self.token_layer_stats(child, token_stats, current_layer+1, max_layers)
                
            if self.is_bottom(child) and child_token_count != 0:
                if self.testing:
                    self.occurance_contents += child.get_text() + '\n'
                    
                curr_token_count += child_token_count

        token_stats[current_layer] += curr_token_count

        return curr_token_count


    def is_bottom(self, element):
        return len(element.contents) == 1 and not isinstance(element.contents[0], bs4.element.Tag)
    
    def collect_script_tags(self, elements):
        script_tags = elements.find_all('script')
        return script_tags


    def print_stats(self, stats):
        print('\n------------------ stats -------------------')
        print(f"{stats}")
        count = sum([count for _, count in stats.items()])
        print(f'total count:{count}')

    
    # def find_all_text_occurence(self, element, token):
    #     token_occurrences = element.find_all(string=lambda text: token in text)
    #     return token_occurrences
    
        