import os
import re
import matplotlib.pyplot as plt
import numpy as np
import argparse
from csv_process_dir import csv_process_dir


def main(e2e_slo):
    # 修改为timestamp目录
    BASE_DIR = '/home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp'
    # 根据目录结构调整算法列表（注意leasted_loaded的拼写）
    ALGORITHMS = ['latency_based', 'leasted_loaded', 'sla_elrar', 'weight_based']
    ALGORITHM_NAMES = {
        'latency_based': 'latency based',
        'leasted_loaded': 'leasted loaded',  # 保持目录中的原始拼写
        'sla_elrar': 'sla elrar',
        'weight_based': 'weight based'
    }
    COLORS = ['blue', 'green', 'red', 'purple']
    MARKERS = ['o', 's', '^', 'D']

    # 更新图表标题和文件名，反映采样率主题
    METRICS = [
        {'name': 'p50', 'label': 'P50 latency(s)', 'title': 'Sampling Rate vs P50 Latency', 'filename': 'sampling_rate_p50_comparison.png'},
        {'name': 'p90', 'label': 'P90 latency(s)', 'title': 'Sampling Rate vs P90 Latency', 'filename': 'sampling_rate_p90_comparison.png'},
        {'name': 'p95', 'label': 'P95 latency(s)', 'title': 'Sampling Rate vs P95 Latency', 'filename': 'sampling_rate_p95_comparison.png'},
        {'name': 'p99', 'label': 'P99 latency(s)', 'title': 'Sampling Rate vs P99 Latency', 'filename': 'sampling_rate_p99_comparison.png'},
        {'name': 'slo', 'label': f'SLO achievement({e2e_slo}s)', 'title': 'Sampling Rate vs SLO Achievement', 'filename': 'sampling_rate_slo_comparison.png', 'is_percentage': True}
    ]

    # 存储所有算法的所有指标数据（采样率为键）
    algorithm_metrics = {alg: {metric['name']: {} for metric in METRICS} for alg in ALGORITHMS}

    # 选择需要显示的采样率（根据实际目录中的采样率调整）
    select_sampling_rates = [0.1,0.12,0.14,0.16]

    # 遍历所有算法目录
    for alg in ALGORITHMS:
        alg_dir = os.path.join(BASE_DIR, alg)
        if not os.path.isdir(alg_dir):
            print(f'警告：算法目录 {alg_dir} 不存在，跳过')
            continue

        # 遍历算法目录下的采样率文件夹
        for dir_name in os.listdir(alg_dir):
            dir_path = os.path.join(alg_dir, dir_name)
            if not os.path.isdir(dir_path):
                continue

            # 从文件夹名称提取采样率（匹配最后一个小数）
            # 支持格式如：flowgpt_timestamp_sla_elrar_0.0_0.19
            sampling_rate_match = re.search(r'_(\d+\.\d+)$', dir_name)

            if not sampling_rate_match:
                print(f'警告：无法从 {dir_name} 提取采样率，跳过')
                continue

            try:
                sampling_rate = float(sampling_rate_match.group(1))
                # 检查是否在需要选择的采样率列表中
                if sampling_rate not in select_sampling_rates:
                    continue
            except ValueError:
                print(f'警告：{dir_name} 中的采样率不是有效数字，跳过')
                continue

            # 判断是否存在CSV文件
            csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]
            if not csv_files:
                print(f'警告：{dir_path} 中未找到CSV文件，跳过')
                continue

            # 调用数据处理函数获取指标
            try:
                metrics = csv_process_dir(dir_path, e2e_slo)
                # 存储所有指标数据（以采样率为键）
                algorithm_metrics[alg]['p50'][sampling_rate] = metrics['p50']
                algorithm_metrics[alg]['p90'][sampling_rate] = metrics['p90']
                algorithm_metrics[alg]['p95'][sampling_rate] = metrics['p95']
                algorithm_metrics[alg]['p99'][sampling_rate] = metrics['p99']
                algorithm_metrics[alg]['slo'][sampling_rate] = metrics['slo_attainment']
            except Exception as e:
                print(f'处理 {alg} 采样率={sampling_rate} 时出错: {str(e)}')
                continue

    # 获取所有唯一的采样率并排序
    all_sampling_rates = sorted(set(sr for alg in ALGORITHMS for metric in METRICS for sr in algorithm_metrics[alg][metric['name']].keys()))
    if not all_sampling_rates:
        print('错误: 未找到任何采样率数据，无法绘制图表')
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
            # 获取当前算法在所有采样率下的指标值并排序
            sorted_sampling_rates = sorted(algorithm_metrics[alg][metric_name].keys())
            values = [algorithm_metrics[alg][metric_name][sr] for sr in sorted_sampling_rates]
            # 绘制折线图
            ax.plot(sorted_sampling_rates, values, marker=MARKERS[i], color=COLORS[i], label=ALGORITHM_NAMES[alg], linewidth=2, markersize=8)

        # 图表配置
        ax.set_xlabel('Sampling Rate', fontsize=20)
        ax.set_ylabel(metric['label'], fontsize=20)
        ax.set_title(metric['title'], fontsize=20, pad=20)
        ax.set_xticks(all_sampling_rates)
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.legend(fontsize=16, loc='best')
        ax.grid(True, linestyle='--', alpha=0.7)
        # 扩展x轴范围，使折线更完整
        ax.set_xlim(min(all_sampling_rates)-0.01, max(all_sampling_rates)+0.01)

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
        plt.savefig(output_path, bbox_inches='tight', dpi=600)
        print(f'{metric_name}图表已保存至: {output_path}')
        plt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slo', type=float, default=9.5, help='端到端SLO阈值（秒）')
    args = parser.parse_args()

    main(args.slo)