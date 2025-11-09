import cv2
import os
import glob

def resize_images(srcPath, dstPath, imgFormat, imgWidth, imgHeight):
    # 获取源目录下所有指定格式的图片文件
    img_files = glob.glob(os.path.join(srcPath, f"*.{imgFormat}"))
    
    # 确保目标目录存在
    os.makedirs(dstPath, exist_ok=True)
    
    for img_file in img_files:
        # 读取图片
        img = cv2.imread(img_file)
        if img is None:
            continue  # 跳过无法读取的文件
        
        # 缩放图片到指定尺寸
        resized_img = cv2.resize(img, (imgWidth, imgHeight), interpolation=cv2.INTER_AREA)
        
        # 提取文件名（不含路径）
        filename = os.path.basename(img_file)
        
        # 构建目标路径（保持原始文件名）
        dst_file = os.path.join(dstPath, filename)
        
        # 保存图片（保持原始文件格式）
        cv2.imwrite(dst_file, resized_img)

# 示例用法
if __name__ == "__main__":
    resize_images(
        srcPath="/mnt/data/dataset/train_image",
        dstPath="/mnt/data/dataset/train_image/img/10_woman_woman",
        imgFormat="jpg",
        imgWidth=512,
        imgHeight=512
    )