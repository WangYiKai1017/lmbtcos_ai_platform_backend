"""
Agent调度器测试文件
展示如何使用调度器和Agent类
"""

from .agent_base import AgentBase, DummyAgent
from .scheduler import scheduler
import time


def test_agent_scheduler():
    """
    测试Agent调度器
    """
    print("=== Agent调度器测试 ===")
    
    # 1. 测试创建DummyAgent
    print("\n1. 创建DummyAgent:")
    agent1 = DummyAgent(name="TestAgent1")
    agent2 = DummyAgent(name="TestAgent2")
    print(f"创建的Agent: {agent1}")
    print(f"创建的Agent: {agent2}")
    
    # 2. 测试启动Agent
    print("\n2. 启动Agent:")
    result1 = scheduler.start_agent(agent1)
    result2 = scheduler.start_agent(agent2)
    print(f"启动Agent1结果: {result1}")
    print(f"启动Agent2结果: {result2}")
    
    # 3. 测试获取Agent数量
    print("\n3. 获取Agent数量:")
    count = scheduler.count_agents()
    print(f"当前运行的Agent数量: {count}")
    
    # 4. 测试获取所有Agent
    print("\n4. 获取所有Agent:")
    all_agents = scheduler.get_all_agents()
    for agent_id, agent in all_agents.items():
        print(f"Agent: {agent}")
    
    # 5. 测试获取Agent状态
    print("\n5. 获取Agent状态:")
    status1 = scheduler.get_agent_status(agent1.agent_id)
    status2 = scheduler.get_agent_status(agent2.agent_id)
    print(f"Agent1状态: {status1}")
    print(f"Agent2状态: {status2}")
    
    # 6. 测试获取所有Agent状态
    print("\n6. 获取所有Agent状态:")
    all_status = scheduler.get_all_agents_status()
    for agent_id, status in all_status.items():
        print(f"Agent {agent_id} 状态: {status}")
    
    # 7. 等待一段时间，让Agent运行
    print("\n7. 等待3秒，让Agent运行...")
    time.sleep(3)
    
    # 8. 测试停止单个Agent
    print("\n8. 停止单个Agent:")
    result = scheduler.stop_agent(agent1.agent_id)
    print(f"停止Agent1结果: {result}")
    print(f"当前运行的Agent数量: {scheduler.count_agents()}")
    
    # 9. 等待一段时间，观察剩余Agent
    print("\n9. 等待3秒，观察剩余Agent运行...")
    time.sleep(3)
    
    # 10. 测试停止所有Agent
    print("\n10. 停止所有Agent:")
    stopped_count = scheduler.stop_all_agents()
    print(f"停止的Agent数量: {stopped_count}")
    print(f"当前运行的Agent数量: {scheduler.count_agents()}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_agent_scheduler()
