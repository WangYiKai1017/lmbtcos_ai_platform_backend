"""
需求挖掘Agent模块
包含对话引导者Agent及其相关组件
"""

from .conversation_guide import ConversationGuideAgent
from .models import (
    RequirementPoint,
    ConversationTurn,
    SessionState,
    HandoffArtifact
)
from .prompts import (
    CONVERSATION_GUIDE_PROMPT,
    FIVE_W_ONE_H_QUESTIONS,
    REQUIREMENT_CONFIRMATION_PROMPT,
    CONVERSATION_END_PROMPT,
    CONTEXT_RESET_PROMPT
)

__all__ = [
    # Agent类
    'ConversationGuideAgent',
    # 数据模型
    'RequirementPoint',
    'ConversationTurn',
    'SessionState',
    'HandoffArtifact',
    # 提示词
    'CONVERSATION_GUIDE_PROMPT',
    'FIVE_W_ONE_H_QUESTIONS',
    'REQUIREMENT_CONFIRMATION_PROMPT',
    'CONVERSATION_END_PROMPT',
    'CONTEXT_RESET_PROMPT'
]
