"""
对话引导者Agent测试入口
允许用户在终端中与对话引导者进行交互
"""

import asyncio
import uuid
from conversation_guide import ConversationGuide


async def main():
    """
    主函数
    """
    print("=" * 60)
    print("对话引导者Agent测试")
    print("=" * 60)
    print("这是一个需求挖掘Agent，可以帮您梳理和澄清需求")
    print("输入 'exit' 退出程序")
    print("输入 'reset' 重置对话")
    print("输入 'export' 导出当前需求")
    print("=" * 60)
    
    # 创建对话引导者
    guide = ConversationGuide()
    
    # 生成会话ID
    session_id = str(uuid.uuid4())
    print(f"\n会话ID: {session_id}")
    
    # 开始对话
    print("\nAgent: 您好！我是需求挖掘专家，请问您有什么需求需要帮助梳理？")
    
    while True:
        user_input = input("\n您: ").strip()
        
        if user_input.lower() == "exit":
            print("\n感谢使用对话引导者Agent，再见！")
            break
            
        elif user_input.lower() == "reset":
            session_id = str(uuid.uuid4())
            print(f"\n已重置对话")
            print(f"新会话ID: {session_id}")
            print("Agent: 您好！我是需求挖掘专家，请问您有什么需求需要帮助梳理？")
            continue
            
        elif user_input.lower() == "export":
            state = await guide.get_conversation_state(session_id)
            if state:
                requirements_json = guide.export_requirements(state)
                print("\n需求导出结果:")
                print(requirements_json)
                
                # 保存到文件
                filename = f"requirements_{session_id[:8]}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(requirements_json)
                print(f"\n需求已保存到文件: {filename}")
            else:
                print("\n当前没有可导出的需求")
            continue
            
        elif not user_input:
            print("请输入有效的内容")
            continue
        
        try:
            # 继续对话
            result = await guide.continue_conversation(session_id, user_input)
            
            # 打印Agent的回复
            if result["messages"]:
                last_message = result["messages"][-1]
                if hasattr(last_message, "content") and last_message.content:
                    print(f"\nAgent: {last_message.content}")
            
            # 检查对话是否完成
            if result["is_completed"]:
                print("\n" + "=" * 60)
                print("对话已完成！")
                print("=" * 60)
                print("已提取的需求点:")
                for req in result["requirements"]:
                    print(f"- {req['content']} (优先级: {req['priority']})")
                
                if result["open_questions"]:
                    print("\n待确认的问题:")
                    for q in result["open_questions"]:
                        print(f"- {q['question']}")
                
                print("\n输入 'export' 可以导出完整需求")
                print("输入 'reset' 可以开始新的对话")
                
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            print("请重试或输入 'reset' 重置对话")


if __name__ == "__main__":
    asyncio.run(main())
