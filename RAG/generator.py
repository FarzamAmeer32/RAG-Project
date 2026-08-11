import ollama

def generate_answer(question, reranked_results):
    """
    Generate an answer using the reranked chunks as context via local Ollama.
    """
    context_parts = []

    for score, document, metadata in reranked_results:
        context_parts.append(
            f"""
Section: {metadata['section']}
Title: {metadata['title']}
Page: {metadata['page']}
Source: {metadata['source']}

Content:
{document}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""You are a legal document assistant.

Answer the question using ONLY the provided context.

If the answer cannot be found in the context,
say that the information is not available in the provided document.

Do not make up information.

Question:
{question}

Context:
{context}

Answer:"""

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        options={
            "temperature": 0.2,
            "num_predict": 200,
        }
    )

    return response["message"]["content"].strip()