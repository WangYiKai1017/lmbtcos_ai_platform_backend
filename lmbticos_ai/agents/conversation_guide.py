"""
对话引导者Agent
负责与用户进行多轮对话，挖掘用户的需求
"""

from typing import Annotated, Sequence, TypedDict, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
import json
import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ConversationState(TypedDict):
    """
    对话引导者的状态管理
    """
    messages: Annotated[Sequence[BaseMessage], "对话历史"]
    session_id: str  # 会话ID
    turn_count: int  # 对话轮数
    requirements: list  # 已提取的需求点列表
    open_questions: list  # 待确认的问题列表
    is_completed: bool  # 是否完成对话
    conversation_summary: str  # 当前对话总结沉淀


class RequirementPoint(BaseModel):
    """
    需求点模型
    """
    id: str
    content: str
    category: str  # 功能需求、非功能需求、数据需求等
    priority: str  # Must/Should/Could/Won't
    description: Optional[str] = None


class OpenQuestion(BaseModel):
    """
    待确认问题模型
    """
    id: str
    question: str
    asked_at: str
    answered_at: Optional[str] = None
    answer: Optional[str] = None


class ConversationGuide:
    """
    对话引导者Agent
    """
    
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """
        初始化对话引导者
        """
        # 从环境变量获取大模型配置
        qwen_url = os.getenv("QWEN_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        qwen_apikey = os.getenv("QWEN_APIKEY", "")
        
        self.llm = llm or ChatOpenAI(
            base_url=qwen_url,
            api_key=qwen_apikey,
            model="qwen-turbo",  # 使用通义千问模型
            temperature=0.7
        )
        
        # 创建工具
        self.tools = []
        
        # 从文件加载提示模板
        self.system_prompt = self._load_prompt("conversation_guide_prompt.md")
        self.summary_prompt = self._load_prompt("requirement_summary_prompt.md")
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # 创建LangGraph工作流
        self.workflow = self._build_workflow()
    
    def _load_prompt(self, prompt_file: str) -> str:
        """
        从文件加载prompt
        """
        prompt_path = os.path.join(
            os.path.dirname(__file__),
            "prompts",
            prompt_file
        )
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def _build_workflow(self):
        """
        构建LangGraph工作流
        """
        
        # 定义节点
        async def call_agent(state: ConversationState):
            """
            调用LLM生成响应
            """
            formatted = self.prompt.format_messages(messages=state["messages"])
            llm_with_tools = self.llm.bind_tools(self.tools)
            response = await llm_with_tools.ainvoke(formatted)
            
            # 生成当前对话总结
            summary_prompt = ChatPromptTemplate.from_messages([
                ("system", "请总结以下对话的核心内容，包括已获取的需求要点、缺失的信息和下一步的引导方向。\n\n对话历史："),
                MessagesPlaceholder(variable_name="messages"),
            ])
            
            summary_response = await self.llm.ainvoke(
                summary_prompt.format_messages(messages=state["messages"] + [response])
            )
            
            return {
                "messages": [response],
                "turn_count": state["turn_count"] + 1,
                "conversation_summary": summary_response.content
            }
        
        def should_continue(state: ConversationState):
            """
            判断是否继续对话
            """
            last_message = state["messages"][-1]
            
            # 检查用户是否明确表示结束
            if isinstance(state["messages"][-2], HumanMessage):
                user_input = state["messages"][-2].content.lower()
                if any(phrase in user_input for phrase in ["结束", "完成", "退出"]):
                    return "complete"
            
            # 继续对话（移除了轮数限制，由Agent自行判断）
            return "agent"
        
        async def complete_conversation(state: ConversationState):
            """
            完成对话，总结需求并准备传递给需求分析师
            """
            # 使用预加载的总结提示模板
            summary_prompt = ChatPromptTemplate.from_messages([
                ("system", self.summary_prompt.format(conversation_history="")),
                MessagesPlaceholder(variable_name="messages"),
            ])
            
            structured_llm = self.llm.with_structured_output(dict)
            summary_response = await structured_llm.ainvoke(
                summary_prompt.format_messages(messages=state["messages"])
            )
            
            # 标记为已完成并准备传递给需求分析师
            return {
                "requirements": summary_response.get("requirements", []),
                "open_questions": summary_response.get("open_questions", []),
                "is_completed": True,
                "conversation_summary": state.get("conversation_summary", "")
            }
        
        # 构建图
        workflow = StateGraph(ConversationState)
        workflow.add_node("agent", call_agent)
        workflow.add_node("complete", complete_conversation)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "agent": "agent",
                "complete": "complete"
            }
        )
        workflow.add_edge("complete", END)
        
        # 编译工作流（带持久化）
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    async def start_conversation(self, session_id: str, initial_message: Optional[str] = None) -> dict:
        """
        开始新的对话
        """
        if initial_message:
            messages = [HumanMessage(content=initial_message)]
        else:
            messages = []
        
        config = {"configurable": {"thread_id": session_id}}
        initial_state = {
            "messages": messages,
            "session_id": session_id,
            "turn_count": 0,
            "requirements": [],
            "open_questions": [],
            "is_completed": False
        }
        
        result = await self.workflow.ainvoke(initial_state, config=config)
        return result
    
    async def continue_conversation(self, session_id: str, user_input: str) -> dict:
        """
        继续对话
        """
        config = {"configurable": {"thread_id": session_id}}
        
        # 获取当前状态
        current_state = None
        async for state in self.workflow.stream(None, config=config, stream_mode="values"):
            current_state = state
        
        if not current_state:
            raise ValueError(f"会话 {session_id} 不存在")
        
        # 如果对话已经完成，返回当前状态
        if current_state["is_completed"]:
            return current_state
        
        # 添加用户输入
        new_state = {
            "messages": current_state["messages"] + [HumanMessage(content=user_input)],
            "session_id": session_id,
            "turn_count": current_state["turn_count"],
            "requirements": current_state["requirements"],
            "open_questions": current_state["open_questions"],
            "is_completed": current_state["is_completed"]
        }
        
        result = await self.workflow.ainvoke(new_state, config=config)
        return result
    
    async def get_conversation_state(self, session_id: str) -> Optional[dict]:
        """
        获取对话状态
        """
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            async for state in self.workflow.stream(None, config=config, stream_mode="values"):
                return state
        except Exception:
            return None
    
    def export_requirements(self, state: dict) -> str:
        """
        导出需求为JSON格式
        """
        export_data = {
            "session_id": state["session_id"],
            "total_turns": state["turn_count"],
            "completed_at": datetime.datetime.now().isoformat(),
            "requirements": state["requirements"],
            "open_questions": state["open_questions"]
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
