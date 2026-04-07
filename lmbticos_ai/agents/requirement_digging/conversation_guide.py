"""
对话引导者Agent
负责与用户进行多轮对话，挖掘用户的需求
"""

from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
from .models import RequirementPoint, SessionState, ConversationTurn
from .prompts import CONVERSATION_GUIDE_PROMPT


class ConversationGuideAgent:
    """
    对话引导者Agent，负责与用户进行多轮对话，挖掘用户需求
    """
    
    def __init__(self, name: str = "对话引导者"):
        """
        初始化对话引导者Agent
        :param name: Agent名称
        """
        self.name = name
        self.session_id: Optional[str] = None
        self.session_state: Optional[SessionState] = None
        self.conversation_turns: List[ConversationTurn] = []
        self.requirement_points: List[RequirementPoint] = []
        self.turn_count = 0
        
    def start_session(self, initial_message: str) -> str:
        """
        开始新的会话
        :param initial_message: 用户的初始需求消息
        :return: 引导者的第一个回应
        """
        # 初始化会话
        self.session_id = f"req-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
        self.turn_count = 0
        
        # 创建初始会话状态
        self.session_state = SessionState(
            session_id=self.session_id,
            status="digging",
            current_phase="digging",
            turn_count=self.turn_count,
            last_turn_at=datetime.now(),
            requirements={"must": [], "should": [], "could": []},
            open_questions=[],
            story_cards=[],
            evaluations=[]
        )
        
        # 记录初始对话
        user_turn = ConversationTurn(
            turn_id=f"turn-{self.turn_count}",
            speaker="user",
            content=initial_message,
            timestamp=datetime.now()
        )
        self.conversation_turns.append(user_turn)
        
        # 生成引导者的回应
        response = self._generate_response(initial_message)
        
        # 记录引导者的回应
        agent_turn = ConversationTurn(
            turn_id=f"turn-{self.turn_count + 1}",
            speaker="agent",
            content=response,
            timestamp=datetime.now()
        )
        self.conversation_turns.append(agent_turn)
        
        # 更新会话状态
        self.turn_count += 2
        self.session_state.turn_count = self.turn_count
        self.session_state.last_turn_at = datetime.now()
        
        return response
    
    def continue_session(self, user_message: str) -> str:
        """
        继续会话
        :param user_message: 用户的回应
        :return: 引导者的下一个回应
        """
        if not self.session_state:
            raise ValueError("会话尚未开始，请先调用start_session方法")
        
        # 记录用户的回应
        user_turn = ConversationTurn(
            turn_id=f"turn-{self.turn_count}",
            speaker="user",
            content=user_message,
            timestamp=datetime.now()
        )
        self.conversation_turns.append(user_turn)
        
        # 分析用户的回应，提取需求点
        self._extract_requirements(user_message)
        
        # 检查是否需要上下文重置
        if self._need_context_reset():
            return self._reset_context()
        
        # 生成引导者的回应
        response = self._generate_response(user_message)
        
        # 记录引导者的回应
        agent_turn = ConversationTurn(
            turn_id=f"turn-{self.turn_count + 1}",
            speaker="agent",
            content=response,
            timestamp=datetime.now()
        )
        self.conversation_turns.append(agent_turn)
        
        # 更新会话状态
        self.turn_count += 2
        self.session_state.turn_count = self.turn_count
        self.session_state.last_turn_at = datetime.now()
        
        return response
    
    def _generate_response(self, user_message: str) -> str:
        """
        生成引导者的回应
        :param user_message: 用户的消息
        :return: 引导者的回应
        """
        # 这里简单实现，实际应该使用LLM生成回应
        # 根据5W1H框架提问
        questions = [
            "能具体说说你想要哪些核心功能吗？",
            "目标用户是谁？他们主要使用场景是什么？",
            "内容类型主要是什么？图文、视频还是混合？",
            "需要社交功能吗？比如关注、点赞、评论？",
            "有没有特定的技术栈要求？",
            "项目的时间预算和资源情况如何？"
        ]
        
        # 根据对话轮次选择不同的问题
        question_index = (self.turn_count // 2) % len(questions)
        
        # 检查是否已经收集了足够的信息
        if len(self.requirement_points) > 5:
            return "我已经了解了一些需求，让我帮你梳理一下..."
        
        return questions[question_index]
    
    def _extract_requirements(self, user_message: str) -> List[RequirementPoint]:
        """
        从用户的回应中提取需求点
        :param user_message: 用户的消息
        :return: 提取的需求点列表
        """
        # 这里简单实现，实际应该使用NLP技术提取需求点
        # 示例：从用户消息中提取关键词作为需求点
        keywords = ["功能", "用户", "场景", "内容", "社交", "技术栈", "时间", "资源"]
        
        new_requirements = []
        for keyword in keywords:
            if keyword in user_message:
                # 提取包含关键词的句子片段
                sentences = user_message.split("。")
                for sentence in sentences:
                    if keyword in sentence:
                        requirement = RequirementPoint(
                            requirement_id=f"req-{len(self.requirement_points) + 1}",
                            content=sentence.strip(),
                            category="功能",  # 默认分类，实际应该自动分类
                            priority="should",  # 默认优先级
                            source="user",
                            timestamp=datetime.now()
                        )
                        self.requirement_points.append(requirement)
                        new_requirements.append(requirement)
                        break
        
        return new_requirements
    
    def _need_context_reset(self) -> bool:
        """
        检查是否需要上下文重置
        :return: 是否需要重置
        """
        # 根据对话轮次判断是否需要重置
        if self.turn_count > 30:  # 超过15轮对话（每轮包含用户和Agent的回应）
            return True
        
        # 检查是否已经收集了足够的信息
        if len(self.requirement_points) > 10:
            return True
        
        return False
    
    def _reset_context(self) -> str:
        """
        重置上下文
        :return: 重置后的回应
        """
        # 生成Handoff工件
        handoff = self.generate_handoff()
        
        # 重置会话状态
        self.session_state.status = "complete"
        
        return f"我已经收集了足够的需求信息，现在将转交给需求分析师进行结构化分析。\n\n已收集的需求点：\n{self._format_requirements()}"
    
    def generate_handoff(self) -> Dict[str, Any]:
        """
        生成Handoff工件
        :return: Handoff工件字典
        """
        return {
            "session_id": self.session_id,
            "phase": "digging",
            "turn_count": self.turn_count,
            "requirements_count": len(self.requirement_points),
            "story_cards_count": 0,
            "confirmed_requirements": [req.content for req in self.requirement_points],
            "open_questions": [],
            "user_preferences": {},
            "next_step": "需求分析师进行结构化分析",
            "notes": ""
        }
    
    def get_session_status(self) -> Dict[str, Any]:
        """
        获取会话状态
        :return: 会话状态字典
        """
        if not self.session_state:
            return {"status": "idle"}
        
        return {
            "session_id": self.session_id,
            "status": self.session_state.status,
            "current_phase": self.session_state.current_phase,
            "turn_count": self.session_state.turn_count,
            "last_turn_at": self.session_state.last_turn_at.isoformat(),
            "requirements_count": len(self.requirement_points),
            "conversation_turns": [turn.__dict__ for turn in self.conversation_turns]
        }
    
    def _format_requirements(self) -> str:
        """
        格式化需求点为可读文本
        :return: 格式化后的需求文本
        """
        if not self.requirement_points:
            return "暂无收集到的需求点"
        
        formatted = "\n".join([f"{i+1}. {req.content}" for i, req in enumerate(self.requirement_points)])
        return formatted
    
    def stop_session(self) -> Dict[str, Any]:
        """
        停止会话
        :return: 会话总结信息
        """
        if not self.session_state:
            return {"message": "会话尚未开始"}
        
        # 生成最终的Handoff工件
        handoff = self.generate_handoff()
        
        # 生成会话总结
        summary = {
            "session_id": self.session_id,
            "total_turns": self.turn_count,
            "total_requirements": len(self.requirement_points),
            "handoff": handoff,
            "message": "会话已结束，需求挖掘完成"
        }
        
        # 重置会话状态
        self.session_state.status = "complete"
        
        return summary
