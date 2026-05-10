import time
import streamlit as st
from agent.tools.react_agent import ReactAgent
import os


os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
# 页面配置
st.set_page_config(page_title="扫地机器人智能客服", layout="wide")
st.title("扫地机器人智能客服")

# 初始化agent（只初始化一次，避免卡顿）
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# 渲染历史消息
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 处理用户输入
if prompt := st.chat_input("请输入你的问题"):
    # 1. 保存并显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response_messages=[]
    with st.spinner("思考中..."):
        res_stream=st.session_state["agent"].execute_stream(query=prompt, history=st.session_state["messages"])

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char


        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        # 先把所有chunk拼成完整字符串，再存入
        full_response = "".join(response_messages)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})


