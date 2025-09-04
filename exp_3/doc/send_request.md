# 请求发送
## replay-logs-origin.log 数据集
### flowgpt-timestamp
- sla_elrar
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py --input ~/replay-logs-origin.log --replay-mode timestamp --sample-range 0.0 0.14 --api-base http://localhost:8888/v1 --model meta-llama/Llama-3.1-8B-Instruct --max-tokens 200 --round-duration 60 --max-rounds 7 --detailed-logs /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/sla_elrar/flowgpt_timestamp_sla_elrar_0.0_0.14/ --json-output /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/sla_elrar/flowgpt_timestamp_sla_elrar_0.0_0.14/flowgpt_timestamp_sla_elrar_0.0_0.14.json

- weight_based
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py --input ~/replay-logs-origin.log --replay-mode timestamp --sample-range 0.0 0.14 --api-base http://localhost:8888/v1 --model meta-llama/Llama-3.1-8B-Instruct --max-tokens 200 --round-duration 60 --max-rounds 7 --detailed-logs /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/weight_based/flowgpt_timestamp_weight_based_0.0_0.14/ --json-output /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/weight_based/flowgpt_timestamp_weight_based_0.0_0.14/flowgpt_timestamp_weight_based_0.0_0.14.json

- latency_based
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py --input ~/replay-logs-origin.log --replay-mode timestamp --sample-range 0.0 0.14 --api-base http://localhost:8888/v1 --model meta-llama/Llama-3.1-8B-Instruct --max-tokens 200 --round-duration 60 --max-rounds 7 --detailed-logs /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/latency_based/flowgpt_timestamp_latency_based_0.0_0.14/ --json-output /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/latency_based/flowgpt_timestamp_latency_based_0.0_0.14/flowgpt_timestamp_latency_based_0.0_0.14.json

- least_loaded
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py --input ~/replay-logs-origin.log --replay-mode timestamp --sample-range 0.0 0.14 --api-base http://localhost:8888/v1 --model meta-llama/Llama-3.1-8B-Instruct --max-tokens 200 --round-duration 60 --max-rounds 7 --detailed-logs /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/least_loaded/flowgpt_timestamp_least_loaded_0.0_0.14/ --json-output /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp/least_loaded/flowgpt_timestamp_least_loaded_0.0_0.14/flowgpt_timestamp_least_loaded_0.0_0.14.json

### flowgpt-qps
python3 /home/paperspace/cys/projects/llm-inference-benchmarking/online_replay.py --input ~/replay-logs-origin.log --replay-mode qps --target-qps 7 --sample-range 0 0.3 --api-base http://localhost:8888/v1 --model meta-llama/Llama-3.1-8B-Instruct --max-tokens 200 --round-duration 60 --max-rounds 7 --detailed-logs /home/paperspace/cys/projects/exp_3/logs/ --json-output /home/paperspace/cys/projects/exp_3/logs/flowgpt_qps_7.json

## shareGPT数据集
- sla_elrar
python3 multi-round-qa.py --num-users 10 --num-rounds 5 --qps 12 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/ShareGPT/sla_elrar/share_gpt_qps_sla_elrar_12.csv

- weight_based
python3 multi-round-qa.py --num-users 10 --num-rounds 5 --qps 12 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/ShareGPT/weight_based/sharegpt_qps_weight_based_12.csv

- latency_based
python3 multi-round-qa.py --num-users 10 --num-rounds 5 --qps 7 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/ShareGPT/latency_based/sharegpt_qps_latency_based_7.csv

- least_loaded
python3 multi-round-qa.py --num-users 10 --num-rounds 5 --qps 12 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/ShareGPT/least_loaded/sharegpt_qps_least_loaded_12.csv

## Coder数据集
- (6 5.5)(8,8)(10,10.5)(12,12)
python3 multi-round-qa.py --num-users 6 --num-rounds 1 --qps 5.5 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 350 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 420 --output /home/paperspace/cys/projects/exp_3/result_v2/Coder/sla_elrar/coder_qps_sla_elrar_5_.csv --data_dir Coder.json

python3 multi-round-qa.py --num-users 6 --num-rounds 1 --qps 5.5 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 350 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 420 --output /home/paperspace/cys/projects/exp_3/result_v2/Coder/weight_based/coder_qps_weight_based_5_.csv --data_dir Coder.json

python3 multi-round-qa.py --num-users 12 --num-rounds 1 --qps 12 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 350 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/Coder/latency_based/coder_qps_latency_based_11.csv --data_dir Coder.json

python3 multi-round-qa.py --num-users 8 --num-rounds 1 --qps 8 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 350 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/Coder/least_loaded/coder_qps_least_loaded_7_.csv --data_dir Coder.json

## Arxiv 数据集
(4,4.5)(5,5.5)(6,6.5)(7,7.5)
- sla_elrar
python3 multi-round-qa.py --num-users 6 --num-rounds 1 --qps 6.5 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/Arxiv/sla_elrar/arxiv_qps_sla_elrar_6.csv --data_dir Arxiv_summary.json

- weight_based
python3 multi-round-qa.py --num-users 1 --num-rounds 1 --qps 1.5 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/Arxiv/weight_based/arxiv_qps_weight_based_1.csv --data_dir Arxiv_summary.json

- least_load
python3 multi-round-qa.py --num-users 5 --num-rounds 1 --qps 5.5 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/Arxiv/least_loaded/arxiv_qps_least_loaded_5.csv --data_dir Arxiv_summary.json

- latency_based
python3 multi-round-qa.py --num-users 1 --num-rounds 1 --qps 1.5 --shared-system-prompt 1000 --user-history-prompt 2000 --answer-len 300 --model meta-llama/Llama-3.1-8B-Instruct --base-url http://localhost:8888/v1 --sharegpt --time 300 --output /home/paperspace/cys/projects/exp_3/result_v2/Arxiv/latency_based/arxiv_qps_latency_based_1.csv --data_dir Arxiv_summary.json