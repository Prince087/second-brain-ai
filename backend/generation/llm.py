import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RAG_PROMPT_TEMPLATE = """You are a helpful assistant answering questions based on the user's personal knowledge base.
Answer the question using ONLY the context below. If the answer isn't in the context, say "I don't have information about that in your notes."

Context:
{context}

Question: {question}

Answer:"""

def generate_answer(question: str, retrieved_chunks: list[dict]) -> str:
    # Combine chunks into one context block
    context = "\n\n".join([
        f"[Source: {chunk['doc_id']}]\n{chunk['chunk']}"
        for chunk in retrieved_chunks
    ])

    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content