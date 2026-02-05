"""
AI Chat Assistant Service for Real Estate Consultation

This service provides RAG-based conversational AI to help users with:
- Property recommendations
- Market analysis
- Real estate terminology
- Location comparisons
"""

from typing import List, Dict, Optional
import logging
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from services.llm_service import LLMService
from storage.vector_store import VectorStoreService

logger = logging.getLogger(__name__)


class ChatAssistant:
    """AI Chat Assistant for real estate consultation."""
    
    SYSTEM_PROMPT = """Bạn là trợ lý AI chuyên về bất động sản tại Hà Nội, Việt Nam.

Nhiệm vụ của bạn:
1. Tư vấn mua/bán nhà đất dựa trên ngân sách và nhu cầu của khách hàng
2. Giải thích các thuật ngữ bất động sản (sổ hồng, sổ đỏ, pháp lý, v.v.)
3. So sánh các khu vực/quận khác nhau về giá cả, tiện ích
4. Phân tích xu hướng thị trường dựa trên dữ liệu thực

Quy tắc:
- Luôn trả lời bằng tiếng Việt
- Dựa trên dữ liệu thực từ hệ thống (được cung cấp trong context)
- Nếu không chắc chắn, hãy nói rõ và đề xuất tìm kiếm thêm
- Gợi ý hành động cụ thể (xem tin đăng, lưu tìm kiếm)
- Giữ câu trả lời ngắn gọn, dễ hiểu (2-3 đoạn văn)

Context từ database:
{context}

Lịch sử hội thoại:
{chat_history}
"""

    def __init__(self):
        """Initialize chat assistant."""
        self.llm_service = LLMService()
        self.vector_store = VectorStoreService()
        
    async def get_response(
        self,
        user_message: str,
        chat_history: List[Dict[str, str]] = None,
        user_id: Optional[int] = None
    ) -> str:
        """
        Generate AI response for user message.
        
        Args:
            user_message: User's question/message
            chat_history: Previous conversation history
            user_id: Optional user ID for personalization
            
        Returns:
            AI-generated response
        """
        try:
            # 1. Retrieve relevant context from vector store
            context = await self._get_relevant_context(user_message)
            
            # 2. Format chat history
            history_text = self._format_chat_history(chat_history or [])
            
            # 3. Build prompt
            prompt = self.SYSTEM_PROMPT.format(
                context=context,
                chat_history=history_text
            )
            
            # 4. Generate response
            messages = [
                SystemMessage(content=prompt),
                HumanMessage(content=user_message)
            ]
            
            response = await self.llm_service.chat(messages)
            
            logger.info(f"Chat response generated for user {user_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return "Xin lỗi, tôi gặp sự cố khi xử lý câu hỏi của bạn. Vui lòng thử lại sau."
    
    async def _get_relevant_context(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant listings/data from vector store.
        
        Args:
            query: User's query
            top_k: Number of results to retrieve
            
        Returns:
            Formatted context string
        """
        try:
            # Search vector store for relevant listings
            results = await self.vector_store.search(query, limit=top_k)
            
            if not results:
                return "Không tìm thấy dữ liệu liên quan trong hệ thống."
            
            # Format results as context
            context_parts = []
            for i, result in enumerate(results, 1):
                metadata = result.get('metadata', {})
                context_parts.append(
                    f"{i}. {metadata.get('title', 'N/A')}\n"
                    f"   - Giá: {metadata.get('price_text', 'N/A')}\n"
                    f"   - Diện tích: {metadata.get('area_m2', 'N/A')} m²\n"
                    f"   - Quận: {metadata.get('district', 'N/A')}\n"
                    f"   - Loại: {metadata.get('property_type', 'N/A')}"
                )
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return "Không thể truy xuất dữ liệu từ hệ thống."
    
    def _format_chat_history(self, history: List[Dict[str, str]]) -> str:
        """
        Format chat history for prompt.
        
        Args:
            history: List of message dicts with 'role' and 'message'
            
        Returns:
            Formatted history string
        """
        if not history:
            return "Chưa có lịch sử hội thoại."
        
        formatted = []
        for msg in history[-5:]:  # Only last 5 messages for context
            role = "Người dùng" if msg['role'] == 'user' else "Trợ lý"
            formatted.append(f"{role}: {msg['message']}")
        
        return "\n".join(formatted)
    
    async def get_suggested_questions(self) -> List[str]:
        """
        Get suggested questions for quick replies.
        
        Returns:
            List of suggested question strings
        """
        return [
            "Tôi có 5 tỷ, nên mua nhà ở quận nào?",
            "Sổ hồng và sổ đỏ khác nhau như thế nào?",
            "Giá nhà ở Cầu Giấy hiện tại ra sao?",
            "So sánh Thanh Xuân và Đống Đa",
            "Chung cư 2 phòng ngủ giá bao nhiêu?",
        ]
