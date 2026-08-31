# general-browser-automation

OpenManus 是一个开源的 AI Agent 框架，能够使用多种工具（浏览器、Python 执行、文件操作、网络搜索等）自动完成复杂任务。本项目设计并开发基于OpenManus架构 的自主浏览器 Agent，支持通过浏览器与 Agent 实时交互，同时针对国内网络环境做了适配优化，旨在解决传统 RPA 无法处理的动态网页交互与复杂推理任务（如跨平台比价、竞品分析）。


## 功能特性

- **Web 图形界面**: 基于 FastAPI + Bootstrap 的浏览器端交互界面，通过 SSE 实时推送 Agent 思考过程和工具调用结果
- **ReAct 推理循环**: Agent 遵循 Think → Act → Observe 的标准范式，具备规划、执行和反思能力
- **多模型支持**: 兼容 OpenAI、Azure OpenAI、阿里云 DashScope、Ollama、AWS Bedrock、Jiekou.AI 等多种 LLM API
- **浏览器自动化**: 基于 Playwright，支持网页浏览、表单填写、数据抓取等操作
- **动态网页交互**: 针对反爬、验证码、级联表单等复杂页面，内置五大场景能力——滑块/点选验证码、无限滚动比价、级联表单、多步骤长流程、iframe/Shadow DOM 穿透（受目标站点服务端风控影响，详见常见问题）
- **Python 代码执行**: Agent 可以编写并运行 Python 代码来完成数据分析和计算任务
- **文件编辑器**: 基于字符串替换的文件编辑工具，可对本地文件进行精确修改
- **网络搜索**: 支持 Google、DuckDuckGo、Bing、百度等多种搜索引擎
- **MCP 协议支持**: 通过 Model Context Protocol 连接外部工具服务器，扩展 Agent 能力
- **Docker 沙箱**: 支持在隔离的 Docker 容器中执行代码，保障主机安全
- **多 Agent 协作**: 支持规划型多 Agent 工作流（Planning Flow），由主控 Agent 制定计划并调度执行

## 项目结构

```
general-browser-automation/
├── app.py                    # Web GUI 主入口（FastAPI + SSE）
├── main.py                   # CLI 命令行入口
├── run_flow.py               # 多 Agent 协作流程入口
├── run_mcp.py                # MCP Agent 入口
├── run_mcp_server.py         # MCP 服务端启动脚本
├── sandbox_main.py           # 沙箱模式入口
├── requirements.txt          # Python 依赖
├── setup.py                  # 包安装配置
├── Dockerfile                # Docker 镜像构建
│
├── app/                      # 核心代码
│   ├── agent/                # Agent 实现
│   │   ├── base.py           # Agent 抽象基类（状态管理、内存、执行循环）
│   │   ├── react.py          # ReAct 循环实现（Think → Act）
│   │   ├── toolcall.py       # 工具调用 Agent（函数调用路由）
│   │   ├── manus.py          # 主 Agent（集成所有工具 + MCP）
│   │   ├── mcp.py            # MCP 协议 Agent
│   │   ├── browser.py        # 浏览器上下文辅助
│   │   ├── data_analysis.py  # 数据分析专用 Agent
│   │   ├── swe.py            # 软件工程 Agent
│   │   └── sandbox_agent.py  # 沙箱 Agent
│   │
│   ├── tool/                 # 工具集合
│   │   ├── base.py           # 工具基类
│   │   ├── tool_collection.py # 工具集合管理
│   │   ├── bash.py           # Bash 命令执行
│   │   ├── python_execute.py # Python 代码执行
│   │   ├── browser_use_tool.py # 浏览器自动化工具
│   │   ├── web_search.py     # 网络搜索工具
│   │   ├── str_replace_editor.py # 字符串替换文件编辑器
│   │   ├── file_operators.py # 文件操作工具
│   │   ├── crawl4ai.py       # 网页爬取工具
│   │   ├── create_chat_completion.py # LLM 调用工具
│   │   ├── planning.py       # 计划管理工具
│   │   ├── ask_human.py      # 人工询问工具
│   │   ├── terminate.py      # 终止工具
│   │   ├── computer_use_tool.py # 计算机控制工具
│   │   ├── mcp.py            # MCP 客户端工具
│   │   ├── search/           # 搜索引擎实现（Google/Bing/Baidu/DuckDuckGo）
│   │   ├── sandbox/          # 沙箱工具（浏览器/文件/Shell/视觉）
│   │   └── chart_visualization/ # 图表可视化工具（ECharts）
│   │
│   ├── flow/                 # 多 Agent 流程控制
│   │   ├── base.py           # 流程基类
│   │   ├── planning.py       # 规划型流程（制定计划 → 逐步执行）
│   │   └── flow_factory.py   # 流程工厂
│   │
│   ├── prompt/               # Prompt 模板
│   │   ├── manus.py          # Manus Agent 的 System Prompt
│   │   ├── toolcall.py       # 工具调用 Prompt
│   │   ├── planning.py       # 规划 Prompt
│   │   ├── swe.py            # 软件工程 Prompt
│   │   ├── browser.py        # 浏览器操作 Prompt
│   │   ├── mcp.py            # MCP Prompt
│   │   └── visualization.py  # 可视化 Prompt
│   │
│   ├── sandbox/              # Docker 沙箱
│   │   ├── client.py         # 沙箱客户端
│   │   └── core/             # 沙箱核心（终端、异常、管理器）
│   │
│   ├── mcp/                  # MCP 协议服务端
│   ├── daytona/              # Daytona 云沙箱集成
│   ├── config.py             # 配置加载与管理
│   ├── llm.py                # LLM 客户端（多模型适配 + Token 计数）
│   ├── schema.py             # 数据模型（Message、Memory、AgentState 等）
│   ├── logger.py             # 日志管理
│   ├── bedrock.py            # AWS Bedrock 客户端
│   ├── knowledge/            # 浏览器操作知识库
│   ├── utils/                # 通用工具函数（文件操作、结构化日志）
│   └── exceptions.py         # 自定义异常
│
├── config/                   # 配置文件
│   ├── config.toml           # 用户配置（不含密钥，需自行创建）
│   ├── config.example.toml   # 配置模板（Anthropic 直连）
│   ├── config.example-model-*.toml  # 各平台配置模板
│   └── mcp.example.json      # MCP 服务配置模板
│
├── static/                   # Web 前端静态资源
│   ├── main.js               # 前端主逻辑（SSE 事件处理）
│   ├── style.css             # 自定义样式
│   ├── bootstrap.min.css     # Bootstrap 样式
│   ├── marked.min.js         # Markdown 渲染
│   └── purify.min.js         # XSS 过滤
│
├── templates/                # Jinja2 模板
│   └── index.html            # Web GUI 主页面
│
├── workspace/                # Agent 工作目录（运行时生成文件存放处）
└── tests/                    # 测试代码
```

## 快速开始

### 环境要求

- Python >= 3.12
- Windows / macOS / Linux
- （可选）Docker - 用于沙箱模式
- （可选）Node.js - 用于图表可视化工具

### 方式一：使用 uv（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/sc3124038545/general-browser-automation.git
cd general-browser-automation

# 2. 创建虚拟环境并激活
uv venv --python 3.12
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. 安装依赖
uv pip install -r requirements.txt

# 4. 安装浏览器驱动（使用浏览器自动化时需要）
playwright install
```

### 方式二：使用 conda

```bash
# 1. 创建 conda 环境
conda create -n openmanus python=3.12
conda activate openmanus

# 2. 克隆仓库并安装
git clone https://github.com/sc3124038545/general-browser-automation.git
cd general-browser-automation
pip install -r requirements.txt

# 3. 安装浏览器驱动
playwright install
```

### 配置 LLM API

项目需要配置大模型 API 才能运行。在 `config` 目录下创建 `config.toml`：

```bash
cp config/config.example.toml config/config.toml
```

然后编辑 `config/config.toml`，填入你的 API 密钥。以下是常用平台的配置示例：

**阿里云 DashScope（国内推荐）**：

```toml
[llm]
api_type = "openai"
model = "qwen-plus"                              # qwen-turbo / qwen-plus / qwen-max
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "sk-xxxxxxxxxxxxxxxx"                  # 替换为你的 DashScope API Key
max_tokens = 8192
temperature = 0.0

[llm.vision]                                      # 视觉模型，仅滑块/点选验证码场景需要
api_type = "openai"
model = "qwen-vl-plus"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "sk-xxxxxxxxxxxxxxxx"
max_tokens = 8192
temperature = 0.0
```

**OpenAI**：

```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-xxxxxxxxxxxxxxxx"
max_tokens = 4096
temperature = 0.0
```

**Ollama（本地模型）**：

```toml
[llm]
api_type = "ollama"
model = "llama3.2"
base_url = "http://localhost:11434/v1"
api_key = "ollama"
max_tokens = 4096
temperature = 0.0
```

> `[llm.vision]` 为视觉模型，仅滑块/点选验证码场景需要；级联表单、滚动比价等纯文本任务只需配置 `[llm]`。

其他平台（Azure、AWS Bedrock、Jiekou.AI）的配置模板见 `config/` 目录下的 `config.example-model-*.toml` 文件。

## 运行方式

本项目支持五种运行模式，可根据需求选择。

### 1. Web GUI 模式（推荐）

启动带图形界面的 Web 服务，在浏览器中与 Agent 交互：

```bash
python app.py
```

浏览器会自动打开 `http://localhost:5172`。在输入框中描述你的任务，Agent 的思考过程、工具调用和结果会通过 SSE 实时显示在页面上。

> 服务器地址和端口可在 `config/config.toml` 的 `[server]` 节配置。

### 2. CLI 命令行模式

在终端中直接与 Agent 对话：

```bash
python main.py
# 或者带参数运行：
python main.py --prompt "帮我分析当前目录下的 Python 文件"
```

### 3. 多 Agent 协作模式

启动规划型多 Agent 工作流，由主控 Agent 制定计划并调度多个 Agent 执行：

```bash
python run_flow.py
```

在 `config/config.toml` 中可启用数据分析 Agent：

```toml
[runflow]
use_data_analysis_agent = true
```

### 4. MCP 工具模式

通过 Model Context Protocol 连接外部工具：

```bash
# 使用 stdio 连接本地 MCP 服务
python run_mcp.py --connection stdio

# 使用 SSE 连接远程 MCP 服务
python run_mcp.py --connection sse --server-url http://127.0.0.1:8000/sse

# 交互模式
python run_mcp.py -i
```

MCP 服务配置在 `config/mcp.json`（参考 `config/mcp.example.json`）。

### 5. 沙箱模式

在 Docker 容器中安全运行 Agent：

```bash
python sandbox_main.py --prompt "你的任务描述"
```

需先确保 Docker 已安装并运行，且在 `config/config.toml` 中启用沙箱：

```toml
[sandbox]
use_sandbox = true
```

## 核心概念

### Agent 继承体系

```
BaseAgent（抽象基类）
  └── ReActAgent（Think → Act 循环）
        └── ToolCallAgent（工具调用路由）
              ├── Manus（通用 Agent，集成全部工具）
              ├── MCPAgent（基于 MCP 协议的 Agent）
              ├── DataAnalysis（数据分析专用 Agent）
              └── SandboxManus（沙箱 Agent）
```

### ReAct 执行流程

每个 Agent 的执行遵循标准 ReAct 循环：

1. **Think（思考）**: Agent 分析当前状态和历史消息，决定下一步行动
2. **Act（执行）**: 调用选定的工具并获取结果
3. **Observe（观察）**: 将工具执行结果加入上下文，进入下一轮思考

重复此循环直到任务完成或达到最大步数（默认 30 步）。

### 工具系统

所有工具继承自 `BaseTool`，通过 `ToolCollection` 统一管理。Agent 使用 LLM 的 Function Calling 能力选择合适的工具。主要工具包括：

| 工具 | 文件 | 功能 |
|------|------|------|
| PythonExecute | `app/tool/python_execute.py` | 执行 Python 代码 |
| BrowserUseTool | `app/tool/browser_use_tool.py` | 浏览器自动化操作 |
| WebSearch | `app/tool/web_search.py` | 搜索引擎查询 |
| StrReplaceEditor | `app/tool/str_replace_editor.py` | 文件查看/编辑/替换 |
| FileOperators | `app/tool/file_operators.py` | 文件操作 |
| Bash | `app/tool/bash.py` | Shell 命令执行 |
| Crawl4aiTool | `app/tool/crawl4ai.py` | 网页内容爬取 |
| PlanningTool | `app/tool/planning.py` | 任务计划管理 |
| AskHuman | `app/tool/ask_human.py` | 向用户提问 |
| Terminate | `app/tool/terminate.py` | 结束任务 |
| MCPClientTool | `app/tool/mcp.py` | MCP 远程工具代理 |

其中 `BrowserUseTool`（浏览器自动化）针对动态网页交互场景提供了以下专用动作：

| 动作 | 场景 | 说明 |
|------|------|------|
| `solve_slider_captcha` | 滑块验证码 | 视觉识别缺口 + 拟人化轨迹拖拽（极验/易盾） |
| `solve_click_captcha` | 点选验证码 | 视觉识别多个目标点并依次点击 |
| `scroll_and_collect` | 滚动比价 | 无限滚动加载 + LLM 结构化抽取商品列表 |
| `get_dropdown_options` / `select_dropdown_option` | 级联表单 | 读取/选择原生 `<select>`，自动触发级联刷新 |
| `click` / `get_dropdown_options` / `select_dropdown_option`（增强） | iframe/Shadow DOM | 跨 iframe 定位 + 穿透 open shadow DOM |

### 多 Agent 流程

`PlanningFlow` 是多 Agent 协作的核心实现：

1. 用户输入任务描述
2. 主控 Agent 调用 `PlanningTool` 制定详细的执行计划（步骤列表）
3. 流程引擎按计划逐步分配任务给合适的 Agent
4. 每步完成后标记状态，直至计划全部完成

## 参与开发

### 开发环境设置

```bash
# 安装开发依赖
pip install pre-commit
pre-commit install
```

### 代码规范

提交前请运行 pre-commit 检查：

```bash
pre-commit run --all-files
```

项目使用以下工具保证代码质量：
- **black** - 代码格式化
- **isort** - import 排序
- **autoflake** - 移除未使用的 import
- **pre-commit-hooks** - 通用检查（行尾空格、文件结尾换行、YAML 格式等）

### 添加新工具

1. 在 `app/tool/` 下创建新文件，继承 `BaseTool`
2. 实现 `name`、`description`、`parameters` 和 `execute` 方法
3. 在 `app/tool/__init__.py` 中注册
4. 在对应 Agent 的 `available_tools` 中添加

```python
from app.tool.base import BaseTool

class MyNewTool(BaseTool):
    name: str = "my_new_tool"
    description: str = "工具的功能描述"

    async def execute(self, **kwargs) -> str:
        # 实现工具逻辑
        return "result"
```

### 添加新 Agent

1. 在 `app/agent/` 下创建新文件，继承 `ToolCallAgent`
2. 设置 `system_prompt`、`next_step_prompt` 和 `available_tools`
3. 可通过 `Manus.create()` 工厂方法模式来初始化

### 目录说明

- `workspace/` 目录是 Agent 运行时的工作目录，Agent 生成的文件会放在这里
- `logs/` 目录存放运行日志
- `debug_html/` 目录存放浏览器自动化演示页（mock 验证码/级联表单/iframe 等场景）
- `tests/` 目录存放各场景的端到端测试脚本
- `cases/` 目录存放测试用例
- `examples/` 目录存放示例代码

## Docker 部署

```bash
# 构建镜像
docker build -t openmanus-gui .

# 运行容器
docker run -p 5172:5172 -v $(pwd)/config:/app/OpenManus/config openmanus-gui python app.py
```

## 常见问题

**Q: 运行时提示找不到 config.toml？**
A: 需要从 `config/config.example.toml` 复制一份并填入有效的 API 密钥。

**Q: 浏览器自动化不工作？**
A: 确保已安装 Chromium 浏览器和 Playwright 驱动：
```bash
playwright install chromium
```

**Q: 国内无法连接 OpenAI API？**
A: 推荐使用阿里云 DashScope 或配置代理。本项目默认配置使用 DashScope API。

**Q: 如何指定 Agent 的工作目录？**
A: Agent 默认在 `workspace/` 目录下工作。可通过 `config/config.toml` 中的路径相关配置调整。

**Q: 沙箱模式启动失败？**
A: 确保 Docker 已安装并运行，且当前用户有 Docker 操作权限。

**Q: Web 页面中文乱码？**
A: Python 文件统一使用 UTF-8 编码，确保终端/浏览器编码设置正确。

**Q: 滑块/点选验证码在极验、12306 上滑动成功但仍提示失败？**
A: 极验（错误码 113）、12306 易盾（error:TJX9v）等服务端风控会在校验环节拒绝自动化请求，
   属厂商的反自动化固有限制，与本地缺口识别、拖拽轨迹无关。自建 mock 页
   （`debug_html/mock_*_captcha.html`）可完整验证求解逻辑；真实站点能否通过取决于对方风控策略。

**Q: 电商比价在京东/淘宝/拼多多上被拦？**
A: 各大电商反爬强度差异很大。京东、淘宝、拼多多基本会拦截自动化访问；苏宁、当当、
   什么值得买等相对友好，可跑通滚动采集。建议先用 `debug_html/mock_scroll_list.html` 验证流程，
   再针对目标站点评估反爬策略。

## 相关项目

- [OpenManus](https://github.com/FoundationAgents/OpenManus) - 原始项目（命令行版本）
- [OpenManus-RL](https://github.com/OpenManus/OpenManus-RL) - 基于强化学习的 LLM Agent 调优
- [MetaGPT](https://github.com/geekan/MetaGPT) - 多 Agent 元编程框架
- [browser-use](https://github.com/browser-use/browser-use) - 浏览器自动化库
- [crawl4ai](https://github.com/unclecode/crawl4ai) - AI 友好网页爬取

## 致谢

本项目基于 [OpenManus](https://github.com/FoundationAgents/OpenManus) 开发，感谢原作者的杰出工作。同时也感谢 [anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts)、[browser-use](https://github.com/browser-use/browser-use)、[MetaGPT](https://github.com/geekan/MetaGPT) 等项目提供的灵感和基础支持。
