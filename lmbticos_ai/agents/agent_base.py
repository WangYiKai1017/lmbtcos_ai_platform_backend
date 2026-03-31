"""
Agent基类定义
所有具体的Agent都应该继承自这个基类
"""

from abc import ABC, abstractmethod
import threading
import uuid


class AgentBase(ABC):
    """
    Agent基类，定义了Agent的基本接口和行为
    """
    
    def __init__(self, agent_id=None, name=None, config=None):
        """
        初始化Agent
        :param agent_id: Agent唯一标识，如果为None则自动生成
        :param name: Agent名称
        :param config: Agent配置参数
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name or f"Agent_{self.agent_id[:8]}"
        self.config = config or {}
        self.is_running = False
        self.thread = None
        self._lock = threading.Lock()
        
    @abstractmethod
    def run(self):
        """
        Agent的主要运行逻辑，需要被子类实现
        """
        pass
    
    def start(self):
        """
        启动Agent，在独立线程中运行
        """
        with self._lock:
            if not self.is_running:
                self.thread = threading.Thread(target=self._run_wrapper, name=self.name)
                self.thread.daemon = True
                self.is_running = True
                self.thread.start()
                return True
            return False
    
    def stop(self):
        """
        停止Agent
        """
        with self._lock:
            if self.is_running:
                self.is_running = False
                if self.thread and self.thread.is_alive():
                    self.thread.join(timeout=5)  # 等待线程结束，最多等待5秒
                return True
            return False
    
    def _run_wrapper(self):
        """
        运行包装器，处理异常和状态管理
        """
        try:
            self.run()
        except Exception as e:
            print(f"Agent {self.name}运行出错: {e}")
            import traceback
            traceback.print_exc()
        finally:
            with self._lock:
                self.is_running = False
    
    def get_status(self):
        """
        获取Agent状态
        :return: 包含Agent状态信息的字典
        """
        with self._lock:
            return {
                'agent_id': self.agent_id,
                'name': self.name,
                'is_running': self.is_running,
                'thread_alive': self.thread.is_alive() if self.thread else False,
                'config': self.config
            }
    
    def update_config(self, new_config):
        """
        更新Agent配置
        :param new_config: 新的配置参数
        """
        with self._lock:
            self.config.update(new_config)
    
    def __str__(self):
        return f"Agent({self.name}, id={self.agent_id}, running={self.is_running})"


class DummyAgent(AgentBase):
    """
    示例Agent，用于测试
    """
    
    def run(self):
        """
        示例运行逻辑
        """
        import time
        print(f"DummyAgent {self.name} started")
        while self.is_running:
            print(f"DummyAgent {self.name} is running...")
            time.sleep(2)
        print(f"DummyAgent {self.name} stopped")
