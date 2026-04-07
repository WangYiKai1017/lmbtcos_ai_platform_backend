"""
对话引导者Agent演示文件
模拟完整的对话流程，展示Agent的功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from lmbticos_ai.agents.requirement_digging.conversation_guide import ConversationGuideAgent


def demo_conversation():
    """
    演示对话流程
    """
    print("=== 对话引导者Agent演示 ===")
    print("\n模拟一个完整的需求挖掘对话流程")
    print("-" * 60)
    
    # 创建对话引导者Agent实例
    guide = ConversationGuideAgent()
    
    # 模拟用户的初始需求
    initial_message = "我想做一个类似小红书的应用"
    print(f"\n用户：{initial_message}")
    
    # 开始会话
    response = guide.start_session(initial_message)
    print(f"引导者：{response}")
    
    # 模拟几轮对话
    user_messages = [
        "核心功能包括用户注册登录、发布图文内容、关注用户、点赞评论",
        "目标用户主要是年轻女性，使用场景是分享生活方式和购物推荐",
        "内容类型主要是图文，也可以支持短视频",
        "需要社交功能，包括关注、点赞、评论、私信",
        "技术栈方面，希望使用Python后端，React前端，PostgreSQL数据库"
    ]
    
    for user_message in user_messages:
        print(f"\n用户：{user_message}")
        response = guide.continue_session(user_message)
        print(f"引导者：{response}")
    
    # 模拟用户表示没有更多需求
    print(f"\n用户：暂时没有其他需求了")
    response = guide.continue_session("暂时没有其他需求了")
    print(f"引导者：{response}")
    
    # 停止会话并获取总结
    summary = guide.stop_session()
    print(f"\n-" * 60)
    print("会话总结：")
    print(f"- 会话ID：{summary['session_id']}")
    print(f"- 总轮次：{summary['total_turns']}")
    print(f"- 收集需求点：{summary['total_requirements']} 个")
    print(f"\n已收集的需求点：")
    for i, req in enumerate(guide.requirement_points):
        print(f"  {i+1}. {req.content}")
    
    # 生成Handoff工件
    handoff = guide.generate_handoff()
    print(f"\nHandoff工件：")
    print(f"- 阶段：{handoff['phase']}")
    print(f"- 对话轮次：{handoff['turn_count']}")
    print(f"- 需求点数量：{handoff['requirements_count']}")
    print(f"- 已确认需求：{', '.join(handoff['confirmed_requirements']) if handoff['confirmed_requirements'] else '无'}")
    print(f"- 下一步：{handoff['next_step']}")


if __name__ == "__main__":
    demo_conversation()
