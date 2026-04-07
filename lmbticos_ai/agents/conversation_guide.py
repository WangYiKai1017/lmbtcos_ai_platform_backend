"""
对话引导者Agent
负责与用户进行多轮对话，挖掘用户的需求
"""

from typing import Annotated, Sequence, TypedDict, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
import json
import datetime


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
        self.llm = llm or ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7
        )
        
        # 创建工具
        self.tools = []
        
        # 创建提示模板
        self.system_prompt = """
你是一名专业的需求挖掘专家，你的任务是通过多轮对话深入了解用户的需求。

## 核心职责：
1. 与用户进行友好、专业的对话，引导用户清晰地表达需求
2. 系统性地挖掘需求，确保覆盖5W1H（What, Who, When, Where, Why, How）
3. 识别用户需求中的模糊点，提出澄清问题
4. 总结并确认已达成共识的需求
5. 当需求足够清晰时，结束对话并输出结构化的需求清单

## 工作流程：
1. 首先，你需要向用户打招呼并询问基本需求
2. 然后，通过提问深入了解需求的细节
3. 持续追问直到你认为需求已经足够清晰
4. 最后，总结所有需求并确认用户是否满意

## 注意事项：
- 每次只问一个问题，避免信息过载
- 使用通俗易懂的语言，避免专业术语
- 对于复杂需求，引导用户分点描述
- 确认用户的优先级和约束条件
- 记录所有已达成共识的需求点

## 对话结束条件：
- 用户明确表示需求已经说完
- 你已经获取了足够清晰的需求（至少5轮对话）
- 需求覆盖率达到80%以上

请开始与用户的对话，首先询问用户的基本需求。
        """
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # 创建LangGraph工作流
        self.workflow = self._build_workflow()
    
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
            return {
                "messages": [response],
                "turn_count": state["turn_count"] + 1
            }
        
        def should_continue(state: ConversationState):
            """
            判断是否继续对话
            """
            last_message = state["messages"][-1]
            
            # 如果LLM没有工具调用，检查是否应该结束对话
            if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                # 检查对话轮数是否足够
                if state["turn_count"] >= 20:
                    return "complete"
                    
                # 检查用户是否表示结束
                if isinstance(state["messages"][-2], HumanMessage):
                    user_input = state["messages"][-2].content.lower()
                    if any(phrase in user_input for phrase in ["够了", "结束", "完成", "可以了", "就这些"]):
                        return "complete"
            
            # 继续对话
            return "agent"
        
        async def complete_conversation(state: ConversationState):
            """
            完成对话，总结需求
            """
            # 总结需求的提示
            summary_prompt = ChatPromptTemplate.from_messages([
                ("system", "你是一名专业的需求分析师，请总结以下对话中的所有需求点，形成结构化的需求清单。\n\n对话历史："),
                MessagesPlaceholder(variable_name="messages"),
                ("system", "\n\n请输出JSON格式的需求清单，包含以下字段：\n- requirements: 需求点列表，每个需求点包含id、content、category、priority、description\n- open_questions: 待确认问题列表，每个问题包含id、question、asked_at\n- session_id: 会话ID\n- total_turns: 对话总轮数\n- completed_at: 完成时间"),
            ])
            
            structured_llm = self.llm.with_structured_output(dict)
            summary_response = await structured_llm.ainvoke(
                summary_prompt.format_messages(messages=state["messages"])
            )
            
            # 更新状态
            return {
                "requirements": summary_response.get("requirements", []),
                "open_questions": summary_response.get("open_questions", []),
                "is_completed": True
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
