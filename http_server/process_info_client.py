import requests
import time
import json
import threading

class ProcessInfoClient:
    def __init__(self, host="localhost", port=8080, endpoint="/metrics"):
        """
        初始化监控客户端
        :param host: 服务器主机 (默认 localhost)
        :param port: 服务器端口 (默认 8080)
        :param endpoint: API端点 (默认 /metrics)
        """
        self.base_url = f"http://{host}:{port}{endpoint}"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ProcessMonitor/1.0",
            "Accept": "application/json"
        })
    
    def fetch_info(self, timeout=2.0):
        """
        从服务器获取进程信息
        :param timeout: 请求超时时间（秒）
        :return: 包含进程信息的字典
        """
        try:
            response = self.session.get(self.base_url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return None
    
    def continuous_monitoring(self, interval=5, callback=None):
        """
        持续监控进程信息
        :param interval: 轮询间隔（秒）
        :param callback: 处理数据的回调函数
        """
        self._running = True
        
        def monitor_loop():
            while self._running:
                data = self.fetch_info()
                if data and callback:
                    callback(data)
                time.sleep(interval)
        
        self.thread = threading.Thread(target=monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        print(f"✅ 开始监控，每 {interval} 秒获取一次数据")
    
    def stop_monitoring(self):
        """停止持续监控"""
        self._running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        print("🛑 监控已停止")

# 使用示例
if __name__ == "__main__":
    # 1. 创建客户端实例
    client = ProcessInfoClient(port=8080)
    
    # 2. 单次获取示例
    print("=== 单次获取进程信息 ===")
    info = client.fetch_info()
    if info:
        print(json.dumps(info, indent=2))
    
    # 3. 持续监控示例
    print("\n=== 持续监控进程信息 ===")
    
    # 定义处理数据的回调函数
    def process_data(data):
        print(f"\n[{data.get('timestamp', '')}]")
        print(f"PID: {data.get('pid', 'N/A')}")
        print(f"线程数: {data.get('thread_count', 'N/A')}")
        print(f"内存使用: {data.get('memory_usage', 'N/A')} KB")
    
    # 启动持续监控
    client.continuous_monitoring(interval=3, callback=process_data)
    
    # 主线程继续工作
    try:
        # 模拟其他工作
        for i in range(10):
            print(f"主程序工作中... ({i+1}/10)")
            time.sleep(1)
    finally:
        client.stop_monitoring()
        