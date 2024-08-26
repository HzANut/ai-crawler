from database.processor.database_list import generate_path
import glob
import os
from html_token_analyzer.spiders.token_spider import TokenSpider
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def open_folder_and_get_file_list(src_root, web_list):
    swde_crawl_list=generate_path(src_root, web_list)
    
    crawl_html_files = {}

    for folder_name in swde_crawl_list:
        files_list = glob.glob(os.path.join(folder_name, '*'))
        crawl_html_files[folder_name.split('\\')[-2]] = files_list

    return crawl_html_files


def save_graphs_to_pdf(datas_list):
    with PdfPages('token_stats_bar.pdf') as pdf:
        for title, data in datas_list.items():

            plt.figure(figsize=(5, 3))
            bars = plt.bar(data.keys(), data.values(), color='skyblue')

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

            # plt.hist(data, bins=[0, 60, 120, 180, 240, 300], edgecolor='black')

            plt.xlabel('level')
            plt.ylabel('token count')
            plt.title(title)

            plt.tight_layout()
            pdf.savefig()
            plt.close()

def run_spiders():

    crawl_html_files = open_folder_and_get_file_list(r"html_token_analyzer\database\swde", r"html_token_analyzer\database\processor\website_list.txt")
    
    spider = TokenSpider()
    token_stats_map = {}
    for catagory, web_files in crawl_html_files.items():
        for html_file in web_files[:6]:
            with open(html_file, 'r', encoding='utf-8') as html_f:
                print(f'opening: {html_f}')
                content = html_f.read()

            soup = BeautifulSoup(content, 'lxml')
            token_stats = defaultdict(int)
            spider.token_layer_stats(soup, token_stats, 1, 8)
            token_stats_map[html_file.split('\\')[-2] + '/' + html_file.split('\\')[-1]] = dict(token_stats)

    print(token_stats_map)
    save_graphs_to_pdf(token_stats_map)


if __name__=="__main__":
    run_spiders()