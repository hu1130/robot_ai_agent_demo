from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from .agent_tools import rag_summarize, get_user_location, get_user_id, \
    get_current_month, fetch_external_data, fill_context_report, get_weather

from .middleware import monitor_tool,log_before_model,report_prompt_switch



class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_user_location, get_user_id, get_current_month, fetch_external_data, fill_context_report, get_weather],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    def execute_stream(self, query: str, history: list):
        # 1. 正确包装用户输入（用 LangChain 标准的 HumanMessage）
        input_dict = {"messages": []}
        if history:
            input_dict["messages"].extend(history)
        input_dict["messages"].append({"role":"user","content":query})
        
        # 用来过滤重复内容，避免重复打印
        seen_content = set()

        # 2. 遍历 stream 输出，增加空列表安全判断
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            # 安全获取 messages 列表，避免 KeyError 或 IndexError
            messages = chunk.get("messages", [])
            if not messages:
                continue  # 消息列表为空时，跳过当前 chunk

            latest_message = messages[-1]
            if latest_message.content:
                # 先处理内容，过滤掉日志和重复
                content = latest_message.content.strip()

                # 过滤1：去掉工具调用日志（比如"已调用"、"特征"这类调试信息）
                if "已调用" in content or "特征" in content or "工具调用" in content:
                    continue

                # 过滤2：去掉已经输出过的重复内容
                if content in seen_content:
                    continue
                seen_content.add(content)

                # 只yield干净的最终回复
                yield content + "\n"


if __name__ == '__main__':
        agent = ReactAgent()
        query = "给我生成我的使用报告"
        for chunk in agent.execute_stream(query):
            print(chunk, end="", flush=True)



