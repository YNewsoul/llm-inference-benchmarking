import os
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse
from csv_process_dir import csv_process_dir

def main(e2e_slo):

    BASE_DIR = '/home/paperspace/cys/projects/exp_3/result/Flowgpt-qps'
    ALGORITHMS = ['latency_based','least_loaded','sla_elrar','weight_based']
    ALGORITHM_NAMES = {
        'latency_based': 'latency based',
        'least_loaded': 'least loaded',
        'sla_elrar': 'sla elrar',
        'weight_based': 'weight based'
    }
    COLORS = ['blue', 'green', 'red', 'purple']
    MARKERS = ['o', 's', '^', 'D']

    METRICS = [
        {'name': 'p50', 'label': 'P50 latency(s)', 'title': 'Title', 'filename': 'qps_p50_comparison.png'},
        {'name': 'p90', 'label': 'P90 latency(s)', 'title': 'Title', 'filename': 'qps_p90_comparison.png'},
        {'name': 'p95', 'label': 'P95 latency(s)', 'title': 'Title', 'filename': 'qps_p95_comparison.png'},
        {'name': 'p99', 'label': 'P99 latency(s)', 'title': 'Title', 'filename': 'qps_p99_comparison.png'},
        {'name': 'slo', 'label': f'SLO achievement({e2e_slo}s)', 'title': 'Title', 'filename': 'qps_slo_comparison.png', 'is_percentage': True}
    ]

    # 存储所有算法的所有指标数据
    algorithm_metrics = {alg: {metric['name']: {} for metric in METRICS} for alg in ALGORITHMS}

    select_qps=[5,7,9,11]
    # 遍历所有算法目录
    for alg in ALGORITHMS:
        alg_dir = os.path.join(BASE_DIR, alg)
        if not os.path.isdir(alg_dir):
            # 不存在该算法目录
            continue

        # 遍历算法目录下的QPS文件夹
        for dir_name in os.listdir(alg_dir):
            dir_path = os.path.join(alg_dir, dir_name)
            if not os.path.isdir(dir_path):
                continue

            # 从文件夹名称提取QPS值
            qps_match = re.search(r'qps_(?:weight_based|sla_elrar|least_loaded|latency_based)_?(\d+)(?:_cv.*)?$', dir_name)
            if not qps_match:
                continue
            qps = int(qps_match.group(1))
            if qps not in select_qps:
                continue

            # 判断是否存在CSV文件
            csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
            if not csv_files:
                continue

            # 调用数据处理函数获取指标
            try:
                metrics = csv_process_dir(dir_path, e2e_slo)
                # 存储所有指标数据
                algorithm_metrics[alg]['p50'][qps] = metrics['p50']
                algorithm_metrics[alg]['p90'][qps] = metrics['p90']
                algorithm_metrics[alg]['p95'][qps] = metrics['p95']
                algorithm_metrics[alg]['p99'][qps] = metrics['p99']
                algorithm_metrics[alg]['slo'][qps] = metrics['slo_achievement']
            except Exception as e:
                print(f'处理 {alg} QPS={qps} 时出错: {str(e)}')
                continue

    # 获取所有唯一的QPS值并排序
    all_qps = sorted(set(qps for alg in ALGORITHMS for metric in METRICS for qps in algorithm_metrics[alg][metric['name']].keys()))
    if not all_qps:
        print('错误: 未找到任何QPS数据，无法绘制图表')
        exit(1)

    # 为每个指标生成图表
    for metric in METRICS:
        metric_name = metric['name']
        # 创建图表
        fig, ax = plt.subplots(figsize=(8, 7))

        # 为每种算法绘制折线图
        for i, alg in enumerate(ALGORITHMS):
            if not algorithm_metrics[alg][metric_name]:
                continue
            # 获取当前算法在所有QPS下的指标值并排序
            sorted_qps = sorted(algorithm_metrics[alg][metric_name].keys())
            values = [algorithm_metrics[alg][metric_name][qps] for qps in sorted_qps]
            # 绘制折线图
            ax.plot(sorted_qps, values, marker=MARKERS[i], color=COLORS[i], label=ALGORITHM_NAMES[alg], linewidth=2, markersize=8)
            # 添加数据标签
            # for x, y in zip(sorted_qps, values):
            #     fmt = '%.2f%%' if metric.get('is_percentage') else '%.4f'
            #     ax.text(x, y, fmt % y, fontsize=9, ha='center', va='bottom')

        # 图表配置
        ax.set_xlabel('QPS',fontsize=20)
        ax.set_ylabel(metric['label'],fontsize=20)
        ax.set_title(metric['title'],fontsize=20, pad=20)
        ax.set_xticks(all_qps)
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.legend(fontsize=16, loc='best')
        ax.grid(True, linestyle='--', alpha=0.7)
        # 扩展x轴范围，使折线更完整
        ax.set_xlim(min(all_qps)-0.5, max(all_qps)+0.5)  

        # 设置y轴范围
        if metric.get('is_percentage'):
            # SLO达标率固定0-100%
            ax.set_ylim(0, 100)
        else:
            # 延迟指标动态调整
            all_values = []
            for alg in ALGORITHMS:
                all_values.extend([v for v in algorithm_metrics[alg][metric_name].values() if not np.isnan(v)])
            if all_values:
                min_value = min(all_values)
                max_value = max(all_values)
                # 添加一些边距
                ax.set_ylim(min_value * 0.9 if min_value > 0 else 0, max_value * 1.1)
            else:
                ax.set_ylim(0, 1)

        # 保存图表
        output_path = os.path.join(BASE_DIR, metric['filename'])
        plt.savefig(output_path, bbox_inches='tight',dpi=600)
        print(f'{metric_name}图表已保存至: {output_path}')
        plt.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--slo', type=float, default=4.5)
    args = parser.parse_args()

    main(args.slo)