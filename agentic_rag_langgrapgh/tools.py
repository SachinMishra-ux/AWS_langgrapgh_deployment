# tools.py
import re
from langchain_core.tools import tool
from langchain.schema import Document
from typing import List
from agentic_rag_langgrapgh.utils import build_context_from_docs

def register_tools(retriever, llm):
    @tool
    def DocumentSearch(query: str) -> str:
        """Search the zoology PDF index and return an LLM-generated answer based on relevant documents."""
        docs: List[Document] = retriever.get_relevant_documents(query)
        context = build_context_from_docs(docs)

        prompt = (
            f"You are a zoology expert. Based on the context below, answer the user's question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer in a concise and clear manner:"
        )
        return llm.invoke(prompt).content

    @tool
    def QuizGenerator(topic: str) -> str:
        """Generate 3 zoology MCQs without answers."""
        docs = retriever.invoke(topic)
        context = build_context_from_docs(docs)

        prompt = (
            "You are a zoology quiz generator.\n"
            "Based on the topic and context below, generate 3 multiple-choice questions WITHOUT answers or explanations.\n\n"
            "Use this format:\n"
            "1. Question?\n a) ...\n b) ...\n c) ...\n d) ...\n\n"
            "2. Question?\n a) ...\n b) ...\n c) ...\n d) ...\n\n"
            "3. Question?\n a) ...\n b) ...\n c) ...\n d) ...\n\n"
            f"Topic: {topic}\n\nContext:\n{context}"
        )

        response = llm.invoke(prompt).content
        return response.strip()


    @tool
    def QuizEvaluator(input_text: str) -> str:
        """Evaluate user-submitted quiz answers and explain correctness."""
        prompt = (
            "You are a zoology quiz evaluator. Input format:\n"
            "Topic: <topic>\n"
            "Answers: <e.g. 1-a,2-b,3-c>\n\n"
            "For each answer:\n"
            "- Mark ✅ or ❌\n"
            "- Provide the correct answer\n"
            "- Give a one-line zoology-based explanation.\n\n"
            f"Input:\n{input_text}"
        )
        return llm.invoke(prompt).content

    return [DocumentSearch, QuizGenerator, QuizEvaluator]
