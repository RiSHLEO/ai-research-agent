import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from duckduckgo_search import DDGS
import wikipedia

load_dotenv()

# Works both locally and on Streamlit Cloud
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Research Agent", page_icon="🔍")
st.title("🔍 AI Research Agent")
st.write("Ask me to research any topic and I'll search the web and produce a report.")

# ============ TOOL FUNCTIONS ============

def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3, region='wt-wt', safesearch='off'))
        if not results:
            return f"No results found for: {query}"
        output = ""
        for r in results:
            output += f"Title: {r['title']}\n"
            output += f"Summary: {r['body']}\n\n"
        return output
    except Exception as e:
        return f"Search unavailable: {str(e)}"

def wikipedia_search(query: str) -> str:
    try:
        results = wikipedia.search(query)
        if not results:
            return "No Wikipedia results found."
        page = wikipedia.page(results[0])
        return page.summary[:1000]
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"

# ============ TOOL DEFINITIONS FOR OPENAI ============

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for current information, news, and facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wikipedia_search",
            "description": "Get detailed background information from Wikipedia on topics, people, and events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The topic to look up"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression like '100 * 0.15'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# Maps tool name to actual function
tool_map = {
    "web_search": web_search,
    "wikipedia_search": wikipedia_search,
    "calculator": calculate
}

# ============ AGENT LOOP ============

def run_agent(user_query: str, thinking_container):
    messages = [
        {
            "role": "system",
            "content": """You are a thorough research assistant. When given a topic:
1. Search for current information using web_search
2. Get background context using wikipedia_search when relevant
3. Use calculator if any numbers need computing
4. Synthesise everything into a clear, structured report

Always use at least 2 tools before giving your final answer."""
        },
        {"role": "user", "content": user_query}
    ]

    steps = []
    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # No tool calls — agent is done
        if not message.tool_calls:
            return message.content, steps

        # Process each tool call
        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # Log the step
            step = f"🔧 Using {tool_name} with: {tool_args}"
            steps.append(step)
            thinking_container.write(step)

            # Run the tool
            tool_result = tool_map[tool_name](**tool_args)

            # Log result preview
            preview = tool_result[:200] + "..." if len(tool_result) > 200 else tool_result
            steps.append(f"📄 Result: {preview}")
            thinking_container.write(f"📄 Result preview: {preview}")

            # Add result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

    return "Maximum research steps reached. Here is what I found so far.", steps

# ============ MAIN APP ============

def main():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if query := st.chat_input("Ask me to research anything..."):

        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.expander("🔍 Agent research steps", expanded=True):
                thinking_container = st.container()

            with st.spinner("Researching..."):
                try:
                    answer, steps = run_agent(query, thinking_container)
                    st.write(answer)
                except Exception as e:
                    answer = f"Error: {str(e)}"
                    st.error(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()