#!/bin/bash

# 第一个命令 - 使用原始输出文件
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py \
  --input ~/replay-logs-origin.log \
  --replay-mode qps \
  --target-qps 2.5 \
  --sample-range 0 0.1 \
  --api-base http://localhost:8888/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --max-tokens 200 \
  --round-duration 60 \
  --max-rounds 7 \
  --detailed-logs /home/paperspace/cys/projects/exp_3/logs/ \
  --json-output /home/paperspace/cys/projects/exp_3/logs/flowgpt_qps_5.json &

# 第二个命令 - 修改输出目录
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py \
  --input ~/replay-logs-origin.log \
  --replay-mode qps \
  --target-qps 2.5 \
  --sample-range 0 0.1 \
  --api-base http://localhost:8888/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --max-tokens 200 \
  --round-duration 60 \
  --max-rounds 7 \
  --detailed-logs /home/paperspace/cys/projects/exp_3/logs_/ \
  --json-output /home/paperspace/cys/projects/exp_3/logs/flowgpt_qps_5.json &

# 等待所有后台进程完成（可选）
wait
 echo "所有命令已完成"