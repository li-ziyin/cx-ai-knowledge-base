# CX AI Knowledge Base

基于 DeepSeek + RAG 的知识库问答系统：文档上传 → 分块 → 向量化 → 语义检索 → 带来源溯源的回答。

> 这是我的第一个完整 RAG 实现（Python 技术栈）。其工程化升级——Redis Stack 向量检索（HNSW）、结构感知分块、评测驱动调优（Recall@5 / MRR@5 指标）——见姊妹项目 **[AgentFlow](https://github.com/li-ziyin/AgentFlow)**（Spring Boot 4 实现）。

## 功能

- 文档上传（PDF/DOCX/TXT），滑动窗口分块入库（200 字符 / 50 重叠）
- sentence-transformers 多语言向量模型语义检索（top-k 余弦相似度），按相关度排序
- 回答附参考来源溯源
- 问答记录与文档入库日志（SQLAlchemy）
- Vue 3 + Element Plus 前端：对话页 / 文档管理页

## 技术栈与选型理由

| 层 | 选型 | 为什么 |
|---|---|---|
| 后端 | FastAPI + Uvicorn | 轻量异步、自动生成 OpenAPI 文档 |
| 对话 | DeepSeek API | 统一 httpx 调用，流式/非流式 |
| 向量化 | sentence-transformers（paraphrase-multilingual-MiniLM-L12-v2） | 本地推理、零 API 成本，离线可用 |
| 向量存储 | JSON 文件 + 暴力余弦 | MVP 定位：数据量小，暴力扫最快且零运维；升级路径见 AgentFlow 的 HNSW 实现 |
| 持久化 | SQLAlchemy | 问答 / 文档双日志表 |
| 前端 | Vue 3 + Element Plus + Vite | 组件生态成熟，快速搭管理界面 |
| 部署 | Docker Compose | 前后端双容器一键拉起 |

## 快速启动

### 后端

    pip install -r requirements.txt
    python run.py

### 前端

    cd frontend
    npm install
    npm run dev

访问 http://localhost:5173 使用系统。

## 目录结构

```
cx-ai-knowledge-base
├── app/
│   ├── api/            # chat / documents / dashboard / health
│   ├── core/           # 配置、数据库连接
│   ├── models/         # SQLAlchemy 模型（ChatLog / DocumentLog）
│   ├── services/       # deepseek / document / rag
│   └── utils/          # 文本清洗与分块
├── frontend/           # Vue 3 + Element Plus
├── scripts/            # 辅助脚本
├── tests/              # pytest
├── Dockerfile
└── docker-compose.yml
```

## 已知边界（诚实版）

- 固定滑窗分块会在段落中间硬切，跨边界内容检索排序受损（消融对比数据见 AgentFlow 评测）
- 暴力余弦检索复杂度 O(N×dim)，千块级以上应换向量库索引
- 向量库为文件存储，不支持并发写与多实例共享

## 作者

li-ziyin
