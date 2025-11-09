import os
import argparse

def rename_jpg_to_lowercase(folder_path):
    """
    将指定文件夹中所有.JPG文件扩展名重命名为.jpg
    """
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件扩展名是否为.JPG（不区分大小写）
        if filename.lower().endswith('.jpg'):
            # 获取文件完整路径
            old_path = os.path.join(folder_path, filename)
            
            # 跳过目录
            if not os.path.isfile(old_path):
                continue
            
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            
            # 如果扩展名是大写的.JPG
            if ext == '.JPG':
                # 构建新文件名（使用小写扩展名）
                new_filename = name + '.jpg'
                new_path = os.path.join(folder_path, new_filename)
                
                # 避免覆盖已存在的文件
                if os.path.exists(new_path):
                    print(f"跳过 {filename}：目标文件 {new_filename} 已存在")
                    continue
                
                # 执行重命名
                try:
                    os.rename(old_path, new_path)
                    print(f"重命名: {filename} -> {new_filename}")
                except OSError as e:
                    print(f"重命名 {filename} 失败: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将.JPG文件扩展名重命名为.jpg')
    parser.add_argument('folder', help='目标文件夹路径')
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"错误：{args.folder} 不是有效目录")
    else:
        rename_jpg_to_lowercase(args.folder)

        