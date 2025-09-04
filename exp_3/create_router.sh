docker rm -f vllm-router   # 先停掉旧的
# --routing-logic: least_loaded, latency_based, weight_based, elrar
docker run -d \
  --network host \
  --name vllm-router \
  zhangy2259/vllm-router:2025-08-30 \
  --port 8888 \
  --service-discovery static \
  --static-backends "http://65.49.81.73:8769,http://184.105.190.123:8769,http://184.105.190.57:8769" \
  --static-models "meta-llama/Llama-3.1-8B-Instruct,meta-llama/Llama-3.1-8B-Instruct,meta-llama/Llama-3.1-8B-Instruct" \
  --static-model-types "chat" \
  --log-stats \
  --log-stats-interval 2 \
  --engine-stats-interval 2 \
  --request-stats-window 2 \
  --session-key "X-Flow-Conversation-Id" \
  --routing-logic elrar \
  # --engine-weights "{\"http://65.49.81.73:8769\": 3.8, \"http://184.105.190.123:8769\": 0.8,\"http://184.105.190.57:8769\": 1.3}"