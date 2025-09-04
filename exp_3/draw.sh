python draw.py --dir /home/paperspace/cys/projects/exp_3/result_v2/Coder --e2e-slo 12
python draw.py --dir /home/paperspace/cys/projects/exp_3/result_v2/ShareGPT --e2e-slo 10
python draw.py --dir /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp --e2e-slo 9
python draw.py --dir /home/paperspace/cys/projects/exp_3/result/Flowgpt-qps --e2e-slo 4.5

python merge_picture.py -d h --input /home/paperspace/cys/projects/exp_3/picture/Coder
python merge_picture.py -d h --input /home/paperspace/cys/projects/exp_3/picture/ShareGPT
python merge_picture.py -d h --input /home/paperspace/cys/projects/exp_3/picture/Flowgpt-timestamp
python merge_picture.py -d h --input /home/paperspace/cys/projects/exp_3/picture/Flowgpt-qps 

python merge_picture.py -d v --input /home/paperspace/cys/projects/exp_3/picture/merge_horizontally

