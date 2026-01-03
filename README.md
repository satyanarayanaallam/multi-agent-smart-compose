# multi-agent-smart-compose
🧠 Multi-Agent Smart Compose + Review System (LangGraph + MCP)

## Overview
This project implements a multi-agent orchestration pipeline using LangGraph (https://github.com/langchain-ai/langgraph) and MCP (Model Context Protocol). It simulates a Smart Compose system that drafts, refines, fact-checks, and reviews text suggestions through collaborative agents.

> Note: This repository is currently a LangGraph learning playground. The structure below represents the **target design** and will be scaffolded step by step.

## ✨ Key Features
- Modular agents for drafting, styling, fact-checking, and feedback
- Supervisor agent for orchestration and termination logic
- MCP integration for external tool calls (e.g., search, DB)
- Visual workflow support via LangGraph Studio
- Scalable design for production-grade ML pipelines

---

## 🧩 Architecture
```
User → Drafting Agent → Style Agent → Fact-Checking Agent
       ↘ Feedback Agent ↔ Drafting Agent
Supervisor Agent → Output
```
Each agent is a LangGraph node with its own logic and tool access. The Supervisor Agent controls flow termination and output generation.

## 🗂️ Project Structure (Planned)

```
multi-agent-smart-compose/
│
├── agents/
│   ├── drafting_agent.py
│   ├── style_agent.py
│   ├── fact_checking_agent.py
│   ├── feedback_agent.py
│   └── supervisor_agent.py
│
├── tools/
│   ├── search_tool.py
│   ├── style_rules.py
│   └── feedback_metrics.py
│
├── workflows/
│   ├── langgraph_workflow.py
│   └── mcp_config.yaml
│
├── notebooks/
│   └── agent_simulation.ipynb
│
├── docs/
│   ├── architecture_diagram.png
│   └── agent_roles.md
│
├── tests/
│   ├── test_agents.py
│   └── test_workflow.py
│
├── .env
├── requirements.txt
├── README.md
└── run.py
```
## 🚀 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/multi_agent_smart_compose.git
cd multi_agent_smart_compose

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your API keys and MCP config

# Run the workflow (to be added)
python run.py
```

## 🧪 Testing

```bash
pytest tests/
```

---

## 📚 Agent Roles (Planned)
- Drafting Agent: Generates initial text using RAG and user context
- Style Agent: Applies tone/style rules based on user preferences
- Fact-Checking Agent: Validates claims using MCP search tools
- Feedback Agent: Scores drafts and loops back for improvement
- Supervisor Agent: Controls flow, termination, and final output

Detailed agent role descriptions will live in docs/agent_roles.md.

---

## 🛠️ Tech Stack
- LangGraph (LangChain ecosystem)
- Python 3.10+
- Model Context Protocol (MCP)
- LLMs via LangChain (e.g., Google Gemini, OpenAI, Anthropic)
- Optional: LangGraph Studio for visual debugging

---

## 📌 Future Extensions
- Add memory agent for user personalization
- Integrate with Gmail or Slack for real-time suggestions
- Deploy on AWS Lambda + API Gateway