"""
对话引导者Agent测试入口
提供终端交互界面，让用户可以测试对话引导者Agent
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from lmbticos_ai.agents.requirement_digging.conversation_guide import ConversationGuideAgent


def main():
    """
    主函数，提供终端交互界面
    """
    print("=== 对话引导者Agent测试 ===")
    print("\n请输入您的初始需求，或输入 'exit' 退出程序")
    print("-" * 50)
    
    # 创建对话引导者Agent实例
    guide = ConversationGuideAgent()
    
    # 获取用户的初始需求
    initial_message = input("您的需求：")
    
    if initial_message.lower() == 'exit':
        print("程序已退出")
        return
    
    # 开始会话
    response = guide.start_session(initial_message)
    print(f"\n引导者：{response}")
    
    # 进入对话循环
    while True:
        user_input = input("\n您：")
        
        if user_input.lower() == 'exit':
            print("\n结束对话...")
            summary = guide.stop_session()
            print(f"\n会话总结：")
            print(f"- 会话ID：{summary['session_id']}")
            print(f"- 总轮次：{summary['total_turns']}")
            print(f"- 收集需求点：{summary['total_requirements']} 个")
            print("程序已退出")
            return
        elif user_input.lower() == 'status':
            print("\n会话状态：")
            status = guide.get_session_status()
            for key, value in status.items():
                if key != 'conversation_turns':  # 不打印完整对话历史
                    print(f"  {key}: {value}")
            continue
        elif user_input.lower() == 'requirements':
            print("\n已收集的需求点：")
            status = guide.get_session_status()
            if guide.requirement_points:
                for i, req in enumerate(guide.requirement_points):
                    print(f"  {i+1}. {req.content}")
            else:
                print("  暂无收集到的需求点")
            continue
        
        # 继续会话
        response = guide.continue_session(user_input)
        print(f"\n引导者：{response}")
        
        # 检查会话是否结束
        status = guide.get_session_status()
        if status.get('status') == 'complete':
            print("\n-" * 50)
            print("需求挖掘已完成，会话结束")
            summary = guide.stop_session()
            print(f"\n会话总结：")
            print(f"- 会话ID：{summary['session_id']}")
            print(f"- 总轮次：{summary['total_turns']}")
            print(f"- 收集需求点：{summary['total_requirements']} 个")
            print("程序已退出")
            return


if __name__ == "__main__":
    main()
