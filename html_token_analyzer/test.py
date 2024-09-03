import matplotlib.pyplot as plt
import numpy as np
if __name__ == '__main__':


    # 示例 token stats 数据
    token_stats = {
        2: {1: 0, 5: 1, 10: 4, 15: 2},
        3: {1: 0, 5: 3, 10: 6, 15: 1},
        4: {1: 1, 5: 2, 10: 3, 15: 0},
    }

    # 合并所有 level 的 token 统计数据，确定分桶的范围
    all_tokens = []
    for tokens in token_stats.values():
        for token_count, count in tokens.items():
            all_tokens.extend([token_count] * count)

    # 创建 token 数的分桶
    bins = np.histogram_bin_edges(all_tokens, bins='auto')

    # 创建一个数组来存储每个 level 和桶的对应数据
    bucket_counts = {level: np.histogram(list(tokens.keys()), bins=bins, weights=list(tokens.values()))[0] for level, tokens in token_stats.items()}

    # 绘制分组柱状图
    bar_width = 0.2
    x = np.arange(len(bins) - 1)  # 分桶数量
    offset = 0  # x 轴的偏移量

    plt.figure(figsize=(12, 6))

    # 为每个 level 绘制柱状图
    for i, (level, counts) in enumerate(bucket_counts.items()):
        plt.bar(x + offset, counts, width=bar_width, label=f'Level {level}')
        offset += bar_width  # 为下一组柱子增加偏移量

    # 设置 x 轴的刻度和标签
    plt.xticks(x + bar_width, [f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins) - 1)])

    # 添加标题和标签
    plt.title('Grouped Bar Chart of Token Counts by Level')
    plt.xlabel('Token Count Buckets')
    plt.ylabel('Document Count')

    # 显示图例
    plt.legend()

    # 显示图表
    plt.show()
