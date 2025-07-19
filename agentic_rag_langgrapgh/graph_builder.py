import re
from typing import TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from groq_llm import get_groq_llm
from tools import register_tools
from faiss_index import get_retriever

# 1️⃣ Shared memory
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    last_quiz: Optional[str]

# 2️⃣ Init LLM, retriever, and tools
llm = get_groq_llm()
retriever = get_retriever()
tools = register_tools(retriever, llm)

# 3️⃣ General Agent Node
agent_node = create_react_agent(
    llm,
    tools=tools,
    prompt="You are a zoology tutor bot. Use tools to answer questions, generate MCQs, or evaluate quizzes."
)

# 4️⃣ Intro Agent
def intro_agent(state: AgentState) -> AgentState:
    intro_msg = "Hello! I am your Zoology Tutor Bot. I can help with concepts, generate quizzes, or evaluate answers."
    return {
        "messages": state["messages"] + [AIMessage(content=intro_msg)],
        "last_quiz": state["last_quiz"]
    }

# 5️⃣ Document Search Node
def doc_search_node(state: AgentState) -> AgentState:
    query = state["messages"][-1].content
    doc_tool = [t for t in tools if t.name == "DocumentSearch"][0]
    result = doc_tool.invoke(query)
    return {
        "messages": state["messages"] + [AIMessage(content=result)],
        "last_quiz": state["last_quiz"]
    }

# 6️⃣ Quiz Generator Node with proactive prompt
def quiz_generator(state: AgentState) -> AgentState:
    topic = state["messages"][-1].content
    quiz_tool = [t for t in tools if t.name == "QuizGenerator"][0]
    quiz = quiz_tool.invoke(topic)

    proactive_msg = (
        f"{quiz}\n\nOnce ready, submit your answers like:\n"
        "1-a, 2-b, 3-c\nand I will evaluate them for you!"
    )

    return {
        "messages": state["messages"] + [AIMessage(content=proactive_msg)],
        "last_quiz": quiz
    }

# 7️⃣ Quiz Evaluator Node with strict topic detection
def quiz_evaluator(state: AgentState) -> AgentState:
    answer_text = state["messages"][-1].content
    last_quiz = state["last_quiz"]

    if not last_quiz:
        return {
            "messages": state["messages"] + [AIMessage(content="No quiz found in history. Please generate a quiz first.")],
            "last_quiz": last_quiz
        }

    # Strict topic detection from prior messages
    topic = None
    for msg in reversed(state["messages"]):
        content_lower = msg.content.lower()
        if "generate quiz on" in content_lower or "quiz on" in content_lower:
            match = re.search(r'(?:generate quiz on|quiz on)\s+(.+)', content_lower)
            if match:
                topic = match.group(1).strip().capitalize()
                break

    if not topic:
        return {
            "messages": state["messages"] + [AIMessage(content="Could not detect the quiz topic from history. Please regenerate the quiz specifying the topic.")],
            "last_quiz": last_quiz
        }

    input_for_evaluator = (
        f"Topic: {topic}\n"
        f"Quiz:\n{last_quiz}\n\n"
        f"Answers:\n{answer_text}"
    )

    eval_tool = [t for t in tools if t.name == "QuizEvaluator"][0]
    evaluation = eval_tool.invoke(input_for_evaluator)

    return {
        "messages": state["messages"] + [AIMessage(content=evaluation)],
        "last_quiz": last_quiz
    }

# 8️⃣ Smart Router Node
def router_node(state: AgentState) -> str:
    user_input = state["messages"][-1].content

    classification_prompt = f"""
You are an intent classifier for a Zoology Tutor Bot. Classify the user input into:

- "intro": if the user greets like hi, hello.
- "doc_search": if the user asks for concepts, definitions, information.
- "quiz_generator": if the user requests to generate a quiz.
- "quiz_evaluator": if the user provides quiz answers, like:
    - "option a"
    - "answer is..."
    - "1-a, 2-b"
    - "my answers are..."
- "agent": for general conversation or anything else.

User input: "{user_input}"

Only respond with one word: intro, doc_search, quiz_generator, quiz_evaluator, agent.
"""

    response = llm.invoke(classification_prompt)
    classification_result = response.content.strip().lower()

    if classification_result not in ["intro", "doc_search", "quiz_generator", "quiz_evaluator", "agent"]:
        classification_result = "agent"

    return classification_result

# 9️⃣ Build the Graph
graph = StateGraph(AgentState)

graph.add_node("router", lambda x: x)
graph.add_node("intro", intro_agent)
graph.add_node("agent", agent_node)
graph.add_node("doc_search", doc_search_node)
graph.add_node("quiz_generator", quiz_generator)
graph.add_node("quiz_evaluator", quiz_evaluator)

graph.add_conditional_edges("router", router_node, {
    "intro": "intro",
    "agent": "agent",
    "doc_search": "doc_search",
    "quiz_generator": "quiz_generator",
    "quiz_evaluator": "quiz_evaluator"
})

graph.set_entry_point("router")
graph.add_edge("intro", END)
graph.add_edge("agent", END)
graph.add_edge("doc_search", END)
graph.add_edge("quiz_generator", END)
graph.add_edge("quiz_evaluator", END)

def build_graph():
    return graph.compile()
