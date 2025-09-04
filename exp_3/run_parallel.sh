## 同时启动两个客户端发送请求

dataset_dir=Coder
# dataset_dir=ShareGPT

# router_dir=weight_based
# router_dir=sla_elrar
# router_dir=latency_based
router_dir=least_loaded

# dir=sharegpt_qps_sla_elrar_14_cv1_0.0_0.1
# dir=sharegpt_qps_latency_based_12_cv1_0.0_0.1
# dir=sharegpt_qps_least_loaded_12_cv1_0.0_0.1
# dir=sharegpt_qps_weight_based_7_cv1_0.0_0.1

# dir=coder_qps_weight_based_12_cv1_0.0_0.2
# dir=coder_qps_sla_elrar_7_cv1_0.0_0.1
# dir=coder_qps_latency_based_7_cv1_0.0_0.1
dir=coder_qps_least_loaded_7_cv1_0.0_0.1

# dataset=shibing624/sharegpt_gpt4
dataset=ajibawa-2023/Python-Code-23k-ShareGPT

qps=3.5
# max_tokens=300
max_tokens=350
cv=1
sample_range=0.1

# 第一个命令 - 使用原始输出文件
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/exp_dataset_analysis/online_replay_sharedgpt.py \
  --replay-mode qps \
  --target-qps ${qps} \
  --sample-range 0.0 ${sample_range} \
  --api-base http://localhost:8888/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --max-tokens ${max_tokens} \
  --round-duration 60 \
  --max-rounds 7 \
  --detailed-logs /home/paperspace/cys/projects/exp_3/logs_/ \
  --json-output /home/paperspace/cys/projects/exp_3/result/${dataset_dir}/${router_dir}/${dir}/${dir}.json \
  --cv ${cv} \
  --preload-time 20 \
  --dataset ${dataset} &

# 第二个命令 - 修改输出目录
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/exp_dataset_analysis/online_replay_sharedgpt.py \
  --replay-mode qps \
  --target-qps ${qps} \
  --sample-range 0.0 ${sample_range} \
  --api-base http://localhost:8888/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --max-tokens ${max_tokens} \
  --round-duration 60 \
  --max-rounds 7 \
  --detailed-logs /home/paperspace/cys/projects/exp_3/logs/ \
  --json-output /home/paperspace/cys/projects/exp_3/result/${dataset_dir}/${router_dir}/${dir}/${dir}.json \
  --cv ${cv} \
  --preload-time 20 \
  --dataset ${dataset} &

# 等待所有后台进程完成（可选）
wait
 echo "所有命令已完成"