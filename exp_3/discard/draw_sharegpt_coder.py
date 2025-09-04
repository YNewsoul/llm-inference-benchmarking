import os
import glob
import matplotlib.pyplot as plt
import argparse
import json
from csv_process import csv_process_file

def main(args):

    algorithm_dirs = {
        'latency_based': 'latency_based',
        'least_loaded': 'least_loaded',
        'sla_elrar': 'sla_elrar',
        'weight_based': 'weight_based'
    }

    algorithm_data = {
        name: {
            'qps': [],
            'p50': [],
            'p90': [],
            'p95': [],
            'p99': [],
            'slo_attainment': []
        } for name in algorithm_dirs.values()
    }

    for dir_name, display_name in algorithm_dirs.items():
        dir_path = os.path.join(args.dir, dir_name)
        if not os.path.exists(dir_path):
            continue
    
        # 获取该算法下的所有CSV文件
        csv_files = glob.glob(os.path.join(dir_path, '*.csv'))
        if not csv_files:
            continue
        
        # select_qps=[5,7,9,11,12]
        select_qps=[2,3,4,5]

        # 处理每个CSV文件
        algorithm_results = []
        for file in csv_files:
            # 提取QPS值（从文件名中提取数字部分）
            filename = os.path.basename(file)
            # 使用正则表达式提取文件名中的数字作为QPS值
            import re
            qps_match = re.search(r'_(\d+)\.csv$', filename)
            if not qps_match:
                continue
            qps = int(qps_match.group(1))
            if qps not in select_qps:
                continue
        
            # 计算所有需要的指标
            try:
                metrics = csv_process_file(file,args.e2e_slo)
                algorithm_results.append((qps, metrics['p50'], metrics['p90'], metrics['p95'], metrics['p99'], metrics['slo_attainment']))
            except Exception as e:
                continue

        # 按QPS排序并存储结果
        if algorithm_results:
            algorithm_results.sort(key=lambda x: x[0])
            algorithm_data[display_name]['qps'] = [item[0] for item in algorithm_results]
            algorithm_data[display_name]['p50'] = [item[1] for item in algorithm_results]
            algorithm_data[display_name]['p90'] = [item[2] for item in algorithm_results]
            algorithm_data[display_name]['p95'] = [item[3] for item in algorithm_results]
            algorithm_data[display_name]['p99'] = [item[4] for item in algorithm_results]
            algorithm_data[display_name]['slo_attainment'] = [item[5] for item in algorithm_results]
        
        output_json_path = os.path.join(args.dir, 'algorithm_data.json')
        try:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(algorithm_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"写入JSON文件失败: {str(e)}")

    # 生成各个百分位数的图表
    plot_metric(algorithm_data, 'p50', 'P50 latency(s)', 'p50')
    plot_metric(algorithm_data, 'p90', 'P90 latency(s)', 'p90')
    plot_metric(algorithm_data, 'p95', 'P95 latency(s)', 'p95')
    plot_metric(algorithm_data, 'p99', 'P99 latency(s)', 'p99')

    # 生成SLO达成率图表（设置Y轴范围为0-100%）
    plot_metric(algorithm_data, 'slo_attainment', f'Slo attainment ({args.e2e_slo}s) (%)', 'slo', y_lim=(0, 100))
# 图表绘制函数
def plot_metric(algorithm_data, metric_name, y_label, output_suffix, y_lim=None):
    plt.figure(figsize=(8, 7))
    colors = ['blue', 'green', 'red', 'purple']
    markers = ['o', 's', '^', 'D']
    
    # 收集所有唯一的QPS值用于x轴刻度
    all_qps = []
    for algorithm_name, data in algorithm_data.items():
        if data['qps']:
            all_qps.extend(data['qps'])
    unique_qps = sorted(list(set(all_qps)))

    for i, (algorithm_name, data) in enumerate(algorithm_data.items()):
        if data['qps'] and data[metric_name]:
            plt.plot(data['qps'], data[metric_name], marker=markers[i], linestyle='-', color=colors[i], linewidth=2, markersize=8, label=algorithm_name)
            # for x, y in zip(data['qps'], data[metric_name]):
            #     # 格式化数值显示，保留两位小数
            #     label_text = f'{y:.2f}'
            #     # 添加文本标签，颜色与线条颜色一致，稍微偏移避免遮挡
            #     plt.text(x, y, label_text, color=colors[i], fontsize=15, ha='center', va='bottom')
    plt.xlabel('QPS', fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.title('', fontsize=20, pad=20)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=16, loc='best')
    # 设置坐标轴刻度字体大小
    plt.xticks(unique_qps, fontsize=16)
    plt.yticks(fontsize=16)
    if y_lim:
        plt.ylim(y_lim)
    plt.tight_layout()
    
    output_path = f'{args.dir}/algorithm_comparison_{output_suffix}.png'
    plt.savefig(output_path, dpi=900, bbox_inches='tight')
    plt.close()
    print(f'{y_label}图表已保存至: {os.path.abspath(output_path)}')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default='/home/paperspace/cys/projects/exp_3/result_v2/Arxiv')
    parser.add_argument('--e2e-slo', type=float, default=4.0)
    args = parser.parse_args()

    main(args)