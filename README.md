# RAG 知识库问答系统

一个基于检索增强生成（RAG）的本地知识库问答项目。上传文档后，系统会根据文档内容检索相关片段，并调用大模型生成带引用来源的回答。

## 功能

- 上传 `PDF / Word / Markdown / TXT` 文档
- 自动解析文本、切分、向量化并建立索引
- 根据用户问题检索最相关的文档片段
- 调用大模型生成回答
- 返回答案引用的来源片段
- 查询、删除已上传文档

## 技术栈

- 后端：`FastAPI`
- 向量数据库：`Chroma`
- Embedding：`SiliconFlow BAAI/bge-m3`
- LLM：`DeepSeek deepseek-chat`
- 文档解析：`pypdf`、`python-docx`

## 项目结构

app/
  api/           # FastAPI 接口
  schemas/       # 请求和响应模型
  services/      # 文档解析、切分、Embedding、检索、LLM 服务
  config.py      # 配置读取
  main.py        # FastAPI 入口
scripts/         # 命令行测试脚本
data/            # 上传文件和向量数据

## 快速开始

1. 创建虚拟环境

python -m venv .venv
.\.venv\Scripts\Activate.ps1

2. 安装依赖

python -m pip install -r requirements.txt

3. 配置环境变量

复制 `.env.example` 为 `.env`，填写 Embedding 和 LLM 的密钥。

4. 启动服务

uvicorn app.main:app --reload

5. 打开接口文档

http://127.0.0.1:8000/docs

## 主要接口

- `GET  /health`：健康检查
- `POST /api/documents/upload`：上传文档
- `GET  /api/documents`：文档列表
- `DELETE /api/documents/{document_id}`：删除文档
- `POST /api/chat`：知识库问答

## 配置说明

- `EMBEDDING_API_KEY`：Embedding 模型密钥
- `EMBEDDING_BASE_URL`：Embedding 接口地址
- `EMBEDDING_MODEL`：Embedding 模型名
- `LLM_API_KEY`：大模型密钥
- `LLM_BASE_URL`：大模型接口地址
- `LLM_MODEL`：大模型名
- `CHUNK_SIZE`：文本切分大小
- `CHUNK_OVERLAP`：文本重叠长度
- `TOP_K`：检索片段数量
- `CHROMA_DIR`：向量数据库存储路径