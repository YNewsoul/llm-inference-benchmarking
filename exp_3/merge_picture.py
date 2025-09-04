from PIL import Image, ImageDraw, ImageFont, ImageColor
import argparse
import os

Image.MAX_IMAGE_PIXELS = None

def get_image_paths_from_directory(directory):
    """从目录中获取所有图片文件路径并按名称排序"""
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} 不是有效的目录")
    
    image_paths = []
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith(image_extensions):
            image_paths.append(os.path.join(directory, filename))
    
    if not image_paths:
        raise ValueError(f"在目录 {directory} 中未找到图片文件")
    return image_paths


def combine_images_horizontally(input_paths, output_path,dataset):
    """将多张图片横向合并为一张图片"""
    # 打开所有图片并确保它们是RGB模式
    images = []
    for path in input_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"图片文件不存在: {path}")
        img = Image.open(path).convert('RGB')
        images.append(img)

    # 计算合并后图片的尺寸
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    # 创建新图片
    combined_img = Image.new('RGB', (total_width, max_height))

    # 粘贴每张图片
    x_offset = 0
    for img in images:
        combined_img.paste(img, (x_offset, 0))
        x_offset += img.width

        # 保存结果
    if not output_path:
        output_dir = "./picture/merge_horizontally"
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/{str(dataset)}_combined_image_h.png"
    # 保存结果
    combined_img.save(output_path)
    print(f"横向合并完成，图片已保存至: {output_path}")


def combine_images_vertically(input_paths, output_path):
    """将多张图片纵向合并为一张图片"""
    # 打开所有图片并确保它们是RGB模式，同时调整尺寸
    images = []
    for path in input_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"图片文件不存在: {path}")
        img = Image.open(path).convert('RGB')

        images.append(img)

    # 计算合并后图片的尺寸
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights)

    # 创建新图片
    combined_img = Image.new('RGB', (max_width, total_height))

    # 粘贴每张图片
    y_offset = 0
    for img in images:
        # 计算水平居中位置
        x_offset = (max_width - img.width) // 2
        combined_img.paste(img, (x_offset, y_offset))
        y_offset += img.height

    # 保存结果
    if not output_path:
        output_dir = f"./picture/merge_vertically"
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/merge_vertically.png"

    combined_img.save(output_path)
    print(f"纵向合并完成，图片已保存至: {output_path}")
    return combined_img
    
def add_segment_texts(image, horizontal_texts=None, vertical_texts=None, font_path=None, font_size=24):
    """在图片上添加横向和纵向分段文字"""
    horizontal_texts = ['a','b','c','d','e']
    vertical_texts = ['1','2','3','4']
    draw = ImageDraw.Draw(image)
    width, height = image.size
    text_color = (0, 0, 0)  # 黑色文字
    font = None

    # 加载字体
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            # 使用默认字体
            font = ImageFont.load_default()
    except Exception as e:
        font = ImageFont.load_default()
        print(f"字体加载错误: {e}，使用默认字体")

    # 添加横向分段文字 (5等分)
    if horizontal_texts and len(horizontal_texts) == 5:
        segment_width = width / 5
        for i, text in enumerate(horizontal_texts):
            # 使用textbbox替代textsize计算文字尺寸
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            # 计算文字位置 (每段上方中央)
            x = segment_width * i + (segment_width - text_width) / 2
            y = 10  # 距离顶部10像素
            draw.text((x, y), text, font=font, fill=text_color)

    # 添加纵向分段文字 (4等分)
    if vertical_texts and len(vertical_texts) == 4:
        segment_height = height / 4
        for i, text in enumerate(vertical_texts):
            # 使用textbbox替代textsize计算文字尺寸
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            # 计算文字位置 (每段左侧中央)
            x = 10  # 距离左侧10像素
            y = segment_height * i + (segment_height - text_height) / 2
            draw.text((x, y), text, font=font, fill=text_color)
    return image

    
def add_legend(image, legend_text, font_path=None, font_size=20):
    """在图片上方添加图例"""
    draw = ImageDraw.Draw(image)
    width, height = image.size
    text_color = (0, 0, 0)  # 黑色文字
    font = None

    # 加载字体
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
            print(f"无法加载指定字体，使用默认字体。字体路径: {font_path}")
    except Exception as e:
        font = ImageFont.load_default()
        print(f"字体加载错误: {e}，使用默认字体")

    # 计算文字位置 (图片上方中央)
    text_width, text_height = draw.textsize(legend_text, font=font)
    x = (width - text_width) / 2
    y = 10  # 距离顶部10像素
    draw.text((x, y), legend_text, font=font, fill=text_color)

    return image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='将目录下所有图片合并为一张图片（横向或纵向）')
    parser.add_argument('--direction','-d', required=True, choices=['h', 'v'])
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    
    try:

        # 获取目录中的所有图片路径
        image_paths = get_image_paths_from_directory(args.input)
        dataset = os.path.basename(args.input)
        print(f"找到 {len(image_paths)} 张图片，准备{ '横向' if args.direction == 'h' else '纵向' }合并...")
        
        # 根据方向调用相应的合并函数
        if args.direction == 'h':
            combine_images_horizontally(image_paths, args.output,dataset)
        else:
            merged_img = combine_images_vertically(image_paths, args.output)
            merged_img = add_segment_texts(merged_img)
            # merged_img = add_legend(merged_img)
            if not args.output:
                output_dir = f"./picture/merge_vertically"
                os.makedirs(output_dir, exist_ok=True)
                args.output = f"{output_dir}/final.png"
            merged_img.save(args.output)


    except Exception as e:
        print(f"发生错误: {str(e)}")
        exit(1)
"""
    示例用法：
    python merge_picture.py -d h --input /home/paperspace/cys/projects/exp_3/result/Flowgpt-timestamp
"""