扫地机器人智能客服 ReAct Agent

基于 LangChain ReAct + Chroma RAG 的轻量化智能客服系统，支持多工具自动调用、文档知识库检索、流式打字机输出。

> 应届生独立开发项目 | 杭州/上海求职中

---

 核心功能

| 功能 | 说明 |
|------|------|
| 🔧 多工具自动调用 | 天气查询、用户信息查询、售后知识库检索，Agent 自动判断调用顺序 |
| 📚 RAG 知识库问答 | 支持 PDF/TXT/Markdown 上传，自动分段、向量化、检索增强生成回答 |
| ⚡ 流式输出 | Streamlit 打字机效果，实时响应 |
| 🔄 增量更新 | 新增文档后直接写入 Chroma，无需重建全量索引 |
**保存位置**：`robot_ai_agent_demo/README.md`（根目录，是 `agent_project` 里）



