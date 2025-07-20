# server.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from agentic_rag_langgrapgh.graph_builder import build_graph
from agentic_rag_langgrapgh.auth import create_token, get_current_user

# === Init FastAPI ===
load_dotenv(override=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# === Compile the LangGraph ===
compiled_graph = build_graph()

# === In-memory chat state (for demo/testing only) ===
chat_history = []  # List of {"user": ..., "bot": ...}
last_quiz = None

# === Request & Response Schema ===
class ChatAgentRequest(BaseModel):
    query: str

class ChatAgentResponse(BaseModel):
    answer: str
    updated_quiz: str | None = None


@app.get("/")
async def home():
    return "Hello from Ec2"


# === Chat Endpoint ===
@app.post("/chat_agent", response_model=ChatAgentResponse)
async def chat_agent(req: ChatAgentRequest, user=Depends(get_current_user)):
    global chat_history, last_quiz

    user_input = req.query.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Build last 3 interactions (max 6 messages)
    msgs = []
    for turn in chat_history[-3:]:
        if "bot" in turn:
            msgs.append(("assistant", turn["bot"]))
        if "user" in turn:
            msgs.append(("user", turn["user"]))
    msgs.append(("user", user_input))

    # Call LangGraph
    result = compiled_graph.invoke({
        "messages": msgs,
        "last_quiz": last_quiz
    })

    # Extract assistant reply & updated quiz
    assistant_reply = result["messages"][-1].content.strip()
    last_quiz = result.get("last_quiz")

    # Update session memory
    chat_history.append({"user": user_input, "bot": assistant_reply})

    return ChatAgentResponse(answer=assistant_reply, updated_quiz=last_quiz)

# === Token Generator (for frontend auth) ===
@app.get("/token")
async def get_token():
    token = create_token({"sub": "test-user"})
    return {"token": token}

# === Optional Reset Endpoint (for dev/testing only) ===
@app.post("/reset")
async def reset_session(user=Depends(get_current_user)):
    global chat_history, last_quiz
    chat_history.clear()
    last_quiz = None
    return {"message": "Session reset."}

# === Launch App ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot_server:app", host="0.0.0.0", port=8000)

