import torch
import numpy as np

def save_tensor_binary(tensor, filename):
    """
    将PyTorch张量按照指定格式存储为二进制文件
    
    格式: dim_num, dim0, dim1, dim2, ..., data
    
    参数:
        tensor: PyTorch张量
        filename: 输出文件名
    """
    # 确保张量在CPU上并且是连续的
    tensor_cpu = tensor.cpu().contiguous()
    
    # 获取张量的维度和形状
    dim_num = tensor_cpu.dim()
    shape = tensor_cpu.shape
    
    # 写入二进制文件
    with open(filename, 'wb') as f:
        # 写入维度数量（int32）
        np.array(dim_num, dtype=np.int32).tofile(f)
        
        # 写入每个维度的大小（int32数组）
        np.array(shape, dtype=np.int32).tofile(f)
        
        # 对于bfloat16，需要特殊处理
        if tensor_cpu.dtype == torch.bfloat16:
            # 将bfloat16转换为uint16（它们有相同的位表示）
            data_uint16 = tensor_cpu.view(torch.uint16)
            data_np = data_uint16.numpy()
            data_np.tofile(f)
        else:
            # 对于其他数据类型，正常处理
            data_np = tensor_cpu.numpy()
            data_np.tofile(f)

def load_tensor_binary(filename, dtype=torch.bfloat16):
    """
    从二进制文件加载PyTorch张量
    
    参数:
        filename: 输入文件名
        dtype: 期望的数据类型（默认bfloat16）
    
    返回:
        PyTorch张量
    """
    with open(filename, 'rb') as f:
        # 读取维度数量
        dim_num = np.fromfile(f, dtype=np.int32, count=1)[0]
        
        # 读取形状数组
        shape = np.fromfile(f, dtype=np.int32, count=dim_num)
        
        # 计算数据元素总数
        num_elements = np.prod(shape)
        
        # 根据数据类型读取数据
        if dtype == torch.bfloat16:
            # 对于bfloat16，先读取为uint16，然后转换为bfloat16
            data = np.fromfile(f, dtype=np.uint16, count=num_elements)
            # 重塑形状并转换为PyTorch张量
            tensor = torch.from_numpy(data.reshape(shape)).view(torch.bfloat16)
        else:
            # 对于其他数据类型
            if dtype == torch.float32:
                np_dtype = np.float32
            elif dtype == torch.float64:
                np_dtype = np.float64
            elif dtype == torch.int32:
                np_dtype = np.int32
            elif dtype == torch.int64:
                np_dtype = np.int64
            else:
                raise ValueError(f"不支持的 dtype: {dtype}")
            
            data = np.fromfile(f, dtype=np_dtype, count=num_elements)
            tensor = torch.from_numpy(data.reshape(shape)).to(dtype)
        
        return tensor

# 专门为bfloat16优化的版本（更简洁）
def save_bfloat16_tensor_binary(tensor, filename):
    """
    专门用于保存bfloat16张量的函数
    """
    # 确保张量在CPU上并且是连续的
    tensor_cpu = tensor.cpu().contiguous()
    
    # 获取张量的维度和形状
    dim_num = tensor_cpu.dim()
    shape = tensor_cpu.shape
    
    # 将bfloat16转换为uint16（它们有相同的位表示）
    data_uint16 = tensor_cpu.view(torch.uint16)
    data_np = data_uint16.numpy()
    
    # 写入二进制文件
    with open(filename, 'wb') as f:
        # 写入维度数量（int32）
        np.array(dim_num, dtype=np.int32).tofile(f)
        
        # 写入每个维度的大小（int32数组）
        np.array(shape, dtype=np.int32).tofile(f)
        
        # 写入数据（uint16格式的bfloat16数据）
        data_np.tofile(f)

def load_bfloat16_tensor_binary(filename):
    """
    专门用于加载bfloat16张量的函数
    """
    with open(filename, 'rb') as f:
        # 读取维度数量
        dim_num = np.fromfile(f, dtype=np.int32, count=1)[0]
        
        # 读取形状数组
        shape = np.fromfile(f, dtype=np.int32, count=dim_num)
        
        # 计算数据元素总数
        num_elements = np.prod(shape)
        
        # 读取uint16数据并转换为bfloat16
        data = np.fromfile(f, dtype=np.uint16, count=num_elements)
        tensor = torch.from_numpy(data.reshape(shape)).view(torch.bfloat16)
        
        return tensor

# 测试示例
if __name__ == "__main__":
    # 创建bfloat16测试张量（不连续的，在GPU上）
    original_tensor = torch.randn(3, 4, 5, dtype=torch.bfloat16).cuda()
    sliced_tensor = original_tensor[:, 1:3, :]  # 这会创建一个不连续的张量
    
    print("原始张量形状:", sliced_tensor.shape)
    print("数据类型:", sliced_tensor.dtype)
    print("是否连续:", sliced_tensor.is_contiguous())
    print("设备:", sliced_tensor.device)
    
    # 保存张量
    save_bfloat16_tensor_binary(sliced_tensor, "bfloat16_tensor_data.bin")
    
    # 加载张量
    loaded_tensor = load_bfloat16_tensor_binary("bfloat16_tensor_data.bin")
    
    print("\n加载的张量形状:", loaded_tensor.shape)
    print("数据类型:", loaded_tensor.dtype)
    print("是否连续:", loaded_tensor.is_contiguous())
    print("设备:", loaded_tensor.device)
    
    # 验证数据一致性
    if torch.allclose(sliced_tensor.cpu(), loaded_tensor, atol=1e-2):
        print("\n✓ 数据保存和加载成功！")
    else:
        print("\n✗ 数据不一致！")
        print("最大误差:", torch.max(torch.abs(sliced_tensor.cpu() - loaded_tensor)))