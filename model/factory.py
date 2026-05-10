from abc import ABC,abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf
from langchain_community.embeddings import DashScopeEmbeddings
import streamlit as st

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings] | BaseChatModel:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings] | BaseChatModel:
        # 从 Streamlit Secrets 读取 API Key 并传入模型
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=st.secrets["DASH_SCOPE_API_KEY"]
        )

class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings] | BaseChatModel:
        # 同样给 Embedding 模型也加上 Key，避免后续报错
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model"],
            dashscope_api_key=st.secrets["DASH_SCOPE_API_KEY"]
        )

chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingsFactory().generator()