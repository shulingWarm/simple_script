import sys

def time_to_minutes(time_str):
    """将时间字符串（HH:MM）转换为分钟数"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except:
        print("错误：时间格式无效，请使用 HH:MM 格式")
        sys.exit(1)

def minutes_to_time(total_minutes):
    """将分钟数转换为时间字符串（HH:MM）"""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python mid_time.py <起始时间> <结束时间>")
        print("示例：python mid_time.py 8:00 22:00")
        sys.exit(1)
    
    start_time = sys.argv[1]
    end_time = sys.argv[2]
    
    # 转换为分钟数
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    
    # 计算中点（分钟数）
    mid_minutes = (start_minutes + end_minutes) // 2
    
    # 转换回时间格式
    result = minutes_to_time(mid_minutes)
    print(result)