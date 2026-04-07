"""
需求挖掘Agent的数据模型
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid


class RequirementPoint:
    """
    需求点模型
    """
    
    def __init__(self,
                 requirement_id: str,
                 content: str,
                 category: str,
                 priority: str,
                 source: str,
                 timestamp: datetime):
        """
        初始化需求点
        :param requirement_id: 需求点ID
        :param content: 需求内容
        :param category: 需求分类
        :param priority: 需求优先级 (must/should/could)
        :param source: 需求来源 (user/agent)
        :param timestamp: 记录时间
        """
        self.requirement_id = requirement_id
        self.content = content
        self.category = category
        self.priority = priority
        self.source = source
        self.timestamp = timestamp
        self.confirmed = False
        self.confirmed_at: Optional[datetime] = None
        self.notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        :return: 需求点字典
        """
        return {
            "requirement_id": self.requirement_id,
            "content": self.content,
            "category": self.category,
            "priority": self.priority,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "confirmed": self.confirmed,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "notes": self.notes
        }


class ConversationTurn:
    """
    对话轮次模型
    """
    
    def __init__(self,
                 turn_id: str,
                 speaker: str,
                 content: str,
                 timestamp: datetime):
        """
        初始化对话轮次
        :param turn_id: 轮次ID
        :param speaker: 发言人 (user/agent)
        :param content: 发言内容
        :param timestamp: 发言时间
        """
        self.turn_id = turn_id
        self.speaker = speaker
        self.content = content
        self.timestamp = timestamp
        self.processed = False
        self.extracted_requirements: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        :return: 对话轮次字典
        """
        return {
            "turn_id": self.turn_id,
            "speaker": self.speaker,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "processed": self.processed,
            "extracted_requirements": self.extracted_requirements
        }


class SessionState:
    """
    会话状态模型
    """
    
    def __init__(self,
                 session_id: str,
                 status: str,
                 current_phase: str,
                 turn_count: int,
                 last_turn_at: datetime,
                 requirements: Dict[str, List[str]],
                 open_questions: List[Dict[str, Any]],
                 story_cards: List[Dict[str, Any]],
                 evaluations: List[Dict[str, Any]]):
        """
        初始化会话状态
        :param session_id: 会话ID
        :param status: 会话状态 (idle/digging/analyzing/generating/evaluating/complete)
        :param current_phase: 当前阶段
        :param turn_count: 对话轮次数
        :param last_turn_at: 最后一次对话时间
        :param requirements: 需求列表 (must/should/could)
        :param open_questions: 未解决问题列表
        :param story_cards: 生成的故事卡列表
        :param evaluations: 评估结果列表
        """
        self.session_id = session_id
        self.status = status
        self.current_phase = current_phase
        self.turn_count = turn_count
        self.last_turn_at = last_turn_at
        self.requirements = requirements
        self.open_questions = open_questions
        self.story_cards = story_cards
        self.evaluations = evaluations
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        :return: 会话状态字典
        """
        return {
            "session_id": self.session_id,
            "status": self.status,
            "current_phase": self.current_phase,
            "turn_count": self.turn_count,
            "last_turn_at": self.last_turn_at.isoformat(),
            "requirements": self.requirements,
            "open_questions": self.open_questions,
            "story_cards": self.story_cards,
            "evaluations": self.evaluations,
            "created_at": self.created_at.isoformat()
        }


class HandoffArtifact:
    """
    Handoff工件模型
    """
    
    def __init__(self,
                 session_id: str,
                 phase: str,
                 turn_count: int,
                 requirements_count: int,
                 story_cards_count: int,
                 confirmed_requirements: List[str],
                 open_questions: List[Dict[str, Any]],
                 user_preferences: Dict[str, Any],
                 next_step: str,
                 notes: str):
        """
        初始化Handoff工件
        :param session_id: 会话ID
        :param phase: 当前阶段
        :param turn_count: 对话轮次数
        :param requirements_count: 需求点数量
        :param story_cards_count: 故事卡数量
        :param confirmed_requirements: 已确认的需求列表
        :param open_questions: 未解决问题列表
        :param user_preferences: 用户偏好
        :param next_step: 下一步计划
        :param notes: 注意事项
        """
        self.session_id = session_id
        self.phase = phase
        self.turn_count = turn_count
        self.requirements_count = requirements_count
        self.story_cards_count = story_cards_count
        self.confirmed_requirements = confirmed_requirements
        self.open_questions = open_questions
        self.user_preferences = user_preferences
        self.next_step = next_step
        self.notes = notes
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        :return: Handoff工件字典
        """
        return {
            "session_id": self.session_id,
            "phase": self.phase,
            "turn_count": self.turn_count,
            "requirements_count": self.requirements_count,
            "story_cards_count": self.story_cards_count,
            "confirmed_requirements": self.confirmed_requirements,
            "open_questions": self.open_questions,
            "user_preferences": self.user_preferences,
            "next_step": self.next_step,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }
