dataset_dir=Coder
# dataset_dir=ShareGPT
# dataset_dir=Reasoning

# router_dir=weight_based
# router_dir=least_loaded
router_dir=sla_elrar
# router_dir=latency_based

# dir=sharegpt_qps_sla_elrar_5_cv1_0.0_0.1
# dir=sharegpt_qps_latency_based_5_cv1_0.0_0.1
# dir=sharegpt_qps_least_loaded_5_cv1_0.0_0.1
# dir=sharegpt_qps_weight_based_5_cv1_0.0_0.1

# dir=coder_qps_weight_based_5_cv1_0.0_0.1
dir=coder_qps_sla_elrar_12__0.0_1
# dir=coder_qps_latency_based_5_cv1_0.0_0.1
# dir=coder_qps_least_loaded_5_cv1_0.0_1

# dir=reasoning_qps_weight_based_0.3_cv0.0_0.0_0.5

# dataset=shibing624/sharegpt_gpt4
dataset=ajibawa-2023/Python-Code-23k-ShareGPT
# dataset=simplescaling/s1K

qps=12
# max_tokens=300
max_tokens=350
# max_tokens=6000
cv=0.5
sample_range=1

python3 /home/paperspace/cys/projects/llm-inference-benchmarking/exp_dataset_analysis/online_replay_sharedgpt.py \
  --replay-mode qps \
  --target-qps ${qps} \
  --sample-range 0.0 ${sample_range} \
  --api-base http://localhost:8888/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --max-tokens ${max_tokens} \
  --round-duration 60 \
  --max-rounds 5 \
  --detailed-logs /home/paperspace/cys/projects/exp_3/result_v2/${dataset_dir}/${router_dir}/${dir}/ \
  --json-output /home/paperspace/cys/projects/exp_3/result_v2/${dataset_dir}/${router_dir}/${dir}/${dir}.json \
  --cv ${cv} \
  --preload-time 20 \
  --dataset ${dataset}