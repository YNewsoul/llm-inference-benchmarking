#!/usr/bin/env bash
# run_vllm.sh
# 按需把 ${port} 改成具体端口，或者通过命令行 ./run_vllm.sh 8769 传入

set -euo pipefail

# 1. 如果没有通过命令行传参，则默认 8769
PORT=${1:-8769}

# 2. 构造容器名（可选）
CONTAINER_NAME="zy_docker"

docker rm -f zy_docker

# 3. 启动容器并执行 vllm serve
docker run --gpus all -it \
  --name "${CONTAINER_NAME}" \
  --ipc=host \
  -p "${PORT}:${PORT}" \
  -v /home/paperspace/cys/projects/vllm-workspace:/vllm-workspace \
  -e VLLM_ENABLE_ELRAR=true \
  -e VLLM_ELRAR_NETWORK_MODE=unicast \
  -e VLLM_ELRAR_GATEWAY_HOST=184.105.190.123 \
  -e VLLM_ELRAR_GATEWAY_PORT=9999 \
  -e VLLM_ELRAR_PUSH_INTERVAL=100 \
  -e VLLM_ELRAR_ENGINE_ID="http://184.105.190.123:${PORT}" \
  -e VLLM_SLA_PRETRAINED_PATH="stable_model_a6000.pkl" \
  --entrypoint /bin/bash \
  zhangy2259/vllm:2025-08-23 \
  -c "vllm serve meta-llama/Llama-3.1-8B-Instruct --max-model-len 10000 --disable-log-requests --port ${PORT} --tensor-parallel-size 2"