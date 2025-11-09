from pathlib import Path

def remove_pycache(directory):
    path = Path(directory)
    for pycache in path.glob("**/__pycache__"):
        # 删除目录及其所有内容
        import shutil
        shutil.rmtree(pycache)
        print(f"已删除: {pycache}")

# 示例：删除当前目录下所有__pycache__
remove_pycache("/mnt/data/workspace/simple_script")

