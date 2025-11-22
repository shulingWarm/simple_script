import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable, Any, Dict

class InfoServer:
    def __init__(self, host: str = "localhost", port: int = 8080):
        """
        初始化监控服务器
        :param host: 监听主机 (默认 localhost)
        :param port: 监听端口 (默认 8080)
        """
        self.host = host
        self.port = port
        self.callback = None
        self.server = None
        self.thread = None

    def set_callback(self, callback: Callable[[], Dict[str, Any]]):
        """
        设置数据回调函数
        :param callback: 返回进程信息的可调用函数
        """
        self.callback = callback

    def start(self):
        """启动后台HTTP服务器"""
        if not self.callback:
            raise ValueError("必须通过 set_callback() 设置回调函数")
        
        # 创建自定义请求处理器
        class Handler(InfoRequestHandler):
            callback = self.callback
        
        # 创建HTTP服务器
        self.server = HTTPServer((self.host, self.port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True  # 设置为守护线程
        self.thread.start()
        print(f"✅ 监控服务器运行在 http://{self.host}:{self.port}")

    def stop(self):
        """停止HTTP服务器"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join()
            print("🛑 监控服务器已停止")

class InfoRequestHandler(BaseHTTPRequestHandler):
    """自定义请求处理器"""
    callback = None
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/metrics':
            try:
                # 通过回调获取进程信息
                data = self.callback()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"回调函数执行失败: {str(e)}")
        else:
            self.send_error(404, "路径不存在")

# 使用示例
if __name__ == "__main__":
    # 1. 创建服务器实例
    server = InfoServer(port=8080)
    
    # 2. 定义数据收集回调函数
    def collect_process_info():
        """示例回调函数，收集进程信息"""
        import os
        import time
        import threading
        return {
            "timestamp": time.time(),
            "pid": os.getpid(),
            "thread_count": threading.active_count(),
            "memory_usage": os.getpid(),
        }
    
    # 3. 设置回调并启动服务器
    server.set_callback(collect_process_info)
    server.start()
    
    # 4. 主进程继续执行其他任务
    print("主进程继续运行...按 Ctrl+C 停止")
    try:
        while True:
            # 模拟主进程工作
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop()

        