# AI Research Agent

An autonomous AI agent that researches any topic by searching the web, 
querying Wikipedia, and performing calculations — then synthesises everything 
into a structured report.

**Live App:** [Click here to view the app](https://ai-research-agent-jq6ykwgp2dpafrhtudzfcd.streamlit.app/)

---

## How It Works

The agent follows a ReAct (Reason and Act) loop — it doesn't follow a fixed 
pipeline. Instead it decides which tools to use, uses them, observes the results, 
and decides what to do next until it has enough information to answer.

1. User submits a research question
2. Agent reasons about which tool to use first
3. Tool runs and returns results
4. Agent reads results and decides if more research is needed
5. Repeats until satisfied
6. Produces a structured research report

The full reasoning process is visible in the expandable "Agent research steps" 
section — showing every tool call and result in real time.

---

## Tools Available to the Agent

- **Web Search** — searches DuckDuckGo for current information and news
- **Wikipedia** — retrieves detailed background information on any topic
- **Calculator** — performs mathematical calculations when needed

---

## Technical Stack

- **LLM:** GPT-3.5-turbo via OpenAI API
- **Tool Calling:** OpenAI function calling API
- **Web Search:** DuckDuckGo Search (free, no API key required)
- **Encyclopedia:** Wikipedia Python API
- **Frontend:** Streamlit
- **Agent Pattern:** ReAct (Reason + Act loop)

---

## Key Features

- Autonomous tool selection — the agent decides which tools to use
- Transparent reasoning — every step visible to the user
- Conversation history — maintains context across messages
- Error handling — gracefully handles tool failures
- Maximum iteration limit — prevents infinite loops and runaway API costs

---

## How to Run Locally

```bash
git clone https://github.com/RiSHLEO/ai-research-agent
cd ai-research-agent
pip install -r requirements.txt
```

Create a `.env` file in the root folder: OPENAI_API_KEY=your-key-here

Then run:
```bash
cd app
streamlit run app.py
```

---

## What I Would Improve With More Time

- Add more tools — news API, stock prices, weather data
- Add source citations with links in the final report
- Implement proper memory so the agent remembers previous research sessions
- Switch to GPT-4 for more complex multi-step reasoning
- Add a report export feature — download as PDF or Word document
- Implement streaming so the final answer appears word by word