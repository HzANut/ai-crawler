from database.processor.database_list import generate_path
import glob
import os
from html_token_analyzer.spiders.token_spider import TokenSpider
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def open_folder_and_get_file_list(src_root, web_list):
    swde_crawl_list=generate_path(src_root, web_list)
    
    crawl_html_files = {}

    for folder_name in swde_crawl_list:
        files_list = glob.glob(os.path.join(folder_name, '*'))
        crawl_html_files[folder_name.split('\\')[-2] + '\\' + folder_name.split('\\')[-1]] = files_list

    return crawl_html_files


def save_graphs_to_pdf(datas_list):
    with PdfPages('token_stats_bar.pdf') as pdf:
        for title, data in datas_list.items():
            # 合并所有 level 的 token 统计数据，确定分桶的范围
            all_tokens = []
            for tokens in data.values():
                for token_count, count in tokens.items():
                    all_tokens.extend([token_count] * count)

            # 创建 token 数的分桶
            bins = np.histogram_bin_edges(all_tokens, bins='auto')

            # 创建一个数组来存储每个 level 和桶的对应数据
            bucket_counts = {level: np.histogram(list(tokens.keys()), bins=bins, weights=list(tokens.values()))[0] for level, tokens in data.items()}

            # 绘制分组柱状图
            bar_width = 0.15
            x = np.arange(len(bins) - 1)  # 分桶数量
            offset = 0  # x 轴的偏移量

            # Choose a color map
            cmap = plt.cm.get_cmap('viridis', len(data))

            # plt.figure(figsize=(12, 6))
            # # Create a subplot with a custom size to make room for the color bar
            fig, ax = plt.subplots(figsize=(12, 6))

            # 为每个 level 绘制柱状图
            for i, (level, counts) in enumerate(bucket_counts.items()):
                plt.bar(x + offset, counts, width=bar_width, label=f'Level {level}', color=cmap(i))
                offset += bar_width  # 为下一组柱子增加偏移量

            # Fix the x-axis labels and ticks by avoiding overlap
            ax.set_xticks(x + bar_width)
            ax.set_xticklabels([f'{int(bins[i])}-{int(bins[i+1])-1}' for i in range(len(bins) - 1)], rotation=45, ha="right")

            # 设置 x 轴的刻度和标签
            plt.xticks(x + bar_width, [f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins) - 1)])

            # 添加标题和标签
            plt.title(title)
            plt.xlabel('Token Count Buckets')
            plt.ylabel('Document Count')

            # Display color bar corresponding to levels
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(data.keys()), vmax=max(data.keys())))
            sm.set_array([])
            
            # Add color bar to the right of the plot
            cbar = fig.colorbar(sm, ax=ax, ticks=list(data.keys()))
            cbar.set_label('Levels')

            pdf.savefig()
            plt.close()


def run_spiders():

    crawl_html_files = open_folder_and_get_file_list(r"html_token_analyzer\database\swde", r"html_token_analyzer\database\processor\website_list.txt")
    
    spider = TokenSpider()
    token_stats_map = {}
    
    for catagory, web_files in crawl_html_files.items():
        level_token_doc_count_maps = {}

        # for html_file in web_files[:6]:
        for html_file in web_files:
            with open(html_file, 'r', encoding='utf-8') as html_f:
                # print(f'opening: {html_f}')
                content = html_f.read()

            soup = BeautifulSoup(content, 'lxml')
            token_stats = defaultdict(int)
            spider.token_layer_stats(soup, token_stats)

            for level, token_count in token_stats.items():
                if level not in level_token_doc_count_maps:
                    level_token_doc_count_maps[level] = {}
                if token_count not in level_token_doc_count_maps[level]:
                    level_token_doc_count_maps[level][token_count] = 0
                if token_count == 0:
                    continue
                level_token_doc_count_maps[level][token_count] += 1

        token_stats_map[catagory] = level_token_doc_count_maps



    print(token_stats_map)
    save_graphs_to_pdf(token_stats_map)
    

if __name__=="__main__":
    run_spiders()