import time
import torch

class TimeProfiler:
    def __init__(self):
        # 存储每个标签的累计时间（单位：秒）
        self.accumulated_time = {}
        # 存储每个标签的开始时间戳
        self.start_times = {}
    
    def begin(self, time_tag: str, cuda_op=False):
        """开始计时指定的标签
        
        Args:
            time_tag: 时间标签
            cuda_op: 是否为 CUDA 操作，如果是则进行 GPU 同步
        """
        if time_tag in self.start_times:
            raise RuntimeError(f"Time tag '{time_tag}' is already being profiled")
        
        # 如果是 CUDA 操作，先进行同步
        if cuda_op:
            torch.cuda.synchronize()
        
        self.start_times[time_tag] = time.time()
    
    def end(self, time_tag: str, cuda_op=False):
        """结束计时并累加时间到指定标签
        
        Args:
            time_tag: 时间标签
            cuda_op: 是否为 CUDA 操作，如果是则进行 GPU 同步
        """
        if time_tag not in self.start_times:
            raise RuntimeError(f"Time tag '{time_tag}' was not started")
        
        # 如果是 CUDA 操作，先进行同步
        if cuda_op:
            torch.cuda.synchronize()
        
        # 计算时间差并累加
        elapsed = time.time() - self.start_times[time_tag]
        self.accumulated_time[time_tag] = self.accumulated_time.get(time_tag, 0) + elapsed
        
        # 移除开始时间记录
        del self.start_times[time_tag]
    
    def get_accum_time(self, time_tag: str) -> float:
        """获取指定标签的累计时间（单位：秒）"""
        return self.accumulated_time.get(time_tag, 0.0)
    
    def print_all_time(self, total_tag: str = None):
        """
        按累计时间从大到小排序打印所有标签的累计时间
        
        Args:
            total_tag: 如果提供，将使用此标签的时间作为总时间计算百分比
                       （标签必须存在）
        """
        if not self.accumulated_time:
            print("No time profiling data available")
            return
        
        # 按累计时间降序排序
        sorted_items = sorted(
            self.accumulated_time.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 处理 total_tag 参数
        total_time = None
        if total_tag is not None:
            if total_tag not in self.accumulated_time:
                raise ValueError(f"Total tag '{total_tag}' not found in profiling data")
            total_time = self.accumulated_time[total_tag]
            print(f"Using '{total_tag}' as total time: {total_time:.6f} seconds")
        
        # 打印结果
        print("Accumulated Time Profiling Results (Sorted by time descending):")
        for tag, tag_time in sorted_items:
            if total_time is not None:
                percentage = (tag_time / total_time) * 100
                if tag == total_tag:
                    print(f"  {tag}: {tag_time:.6f} seconds ({percentage:.2f}%) [TOTAL]")
                else:
                    print(f"  {tag}: {tag_time:.6f} seconds ({percentage:.2f}%)")
            else:
                print(f"  {tag}: {tag_time:.6f} seconds")