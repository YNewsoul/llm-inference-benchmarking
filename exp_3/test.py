from PIL import Image
import os
from merge_picture import add_legend_to_image,add_title_to_image,add_side_title_to_image
# file_path = "/home/paperspace/cys/projects/llm-inference-benchmarking/exp_3/picture/merge_vertically/merge_vertically.png"
file_path = "/home/paperspace/cys/projects/llm-inference-benchmarking/exp_3/picture/Coder/Coder_comparison_p50.png"
img = Image.open(file_path)
add_side_title_to_image(img)
# add_legend_to_image(img)
