from abc import ABC,abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf
from langchain_community.embeddings import DashScopeEmbeddings
import os


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings] | BaseChatModel:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings] | BaseChatModel:
        # 优先读环境变量，没有再尝试从 Secrets 读（线上环境）
        dashscope_api_key = os.getenv("DASH_SCOPE_API_KEY")
        if not dashscope_api_key:
            import streamlit as st
            dashscope_api_key = st.secrets["DASH_SCOPE_API_KEY"]

        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=dashscope_api_key
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings] | BaseChatModel:
        dashscope_api_key = os.getenv("DASH_SCOPE_API_KEY")
        if not dashscope_api_key:
            import streamlit as st
            dashscope_api_key = st.secrets["DASH_SCOPE_API_KEY"]

        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=dashscope_api_key
        )


# 原来的错误写法
# chat_model_name = ChatModelFactory().generator()
# embedding_model_name = EmbeddingsFactory().generator()

# 改成和导入语句一致的名字
chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingsFactory().generator()