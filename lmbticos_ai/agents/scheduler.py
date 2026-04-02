"""
Agent调度器
采用单例模式，负责管理所有Agent的生命周期
"""

import threading
from typing import Dict, Optional
from .agent_base import AgentBase


class AgentScheduler:
    """
    Agent调度器类，采用单例模式
    """
    
    _instance: Optional['AgentScheduler'] = None
    _lock: threading.Lock = threading.Lock()
    
    def __new__(cls):
        """
        单例模式实现
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AgentScheduler, cls).__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        """
        初始化调度器
        """
        self.agents: Dict[str, AgentBase] = {}  # 存储所有Agent，key为agent_id
        self._lock: threading.Lock = threading.Lock()
        print("AgentScheduler initialized")
    
    def start_agent(self, agent: AgentBase) -> bool:
        """
        启动一个Agent
        :param agent: Agent实例
        :return: 成功启动返回True，否则返回False
        """
        with self._lock:
            if agent.agent_id in self.agents:
                print(f"Agent {agent.agent_id} already exists")
                return False
            
            # 启动Agent
            if agent.start():
                self.agents[agent.agent_id] = agent
                print(f"Agent {agent.agent_id} ({agent.name}) started successfully")
                return True
            else:
                print(f"Failed to start Agent {agent.agent_id}")
                return False
    
    def stop_agent(self, agent_id: str) -> bool:
        """
        停止指定的Agent
        :param agent_id: Agent唯一标识
        :return: 成功停止返回True，否则返回False
        """
        with self._lock:
            if agent_id not in self.agents:
                print(f"Agent {agent_id} not found")
                return False
            
            agent = self.agents[agent_id]
            if agent.stop():
                del self.agents[agent_id]
                print(f"Agent {agent_id} ({agent.name}) stopped successfully")
                return True
            else:
                print(f"Failed to stop Agent {agent_id}")
                return False
    
    def stop_all_agents(self) -> int:
        """
        停止所有Agent
        :return: 成功停止的Agent数量
        """
        with self._lock:
            stopped_count = 0
            agent_ids = list(self.agents.keys())  # 复制一份，避免遍历过程中修改字典
            
            for agent_id in agent_ids:
                if self.stop_agent(agent_id):
                    stopped_count += 1
            
            print(f"Stopped {stopped_count} agents")
            return stopped_count
    
    def get_agent(self, agent_id: str) -> Optional[AgentBase]:
        """
        获取指定的Agent
        :param agent_id: Agent唯一标识
        :return: Agent实例或None
        """
        with self._lock:
            return self.agents.get(agent_id)
    
    def get_all_agents(self) -> Dict[str, AgentBase]:
        """
        获取所有Agent
        :return: 所有Agent的字典，key为agent_id
        """
        with self._lock:
            return self.agents.copy()  # 返回副本，避免外部修改
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """
        获取指定Agent的状态
        :param agent_id: Agent唯一标识
        :return: Agent状态字典或None
        """
        agent = self.get_agent(agent_id)
        if agent:
            return agent.get_status()
        return None
    
    def get_all_agents_status(self) -> Dict[str, Dict]:
        """
        获取所有Agent的状态
        :return: 所有Agent的状态字典，key为agent_id
        """
        with self._lock:
            return {
                agent_id: agent.get_status()
                for agent_id, agent in self.agents.items()
            }
    
    def count_agents(self) -> int:
        """
        获取当前运行的Agent数量
        :return: Agent数量
        """
        with self._lock:
            return len(self.agents)
    
    def __str__(self):
        return f"AgentScheduler(running_agents={self.count_agents()})"


# 创建全局调度器实例
scheduler = AgentScheduler()
