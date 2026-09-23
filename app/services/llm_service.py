from openai import OpenAI

from app.config import settings


client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url,
)


SYSTEM_PROMPT = (
    "你是一个只能基于给定资料回答的助手。"
    "如果资料中没有答案，就说“资料中未找到相关内容”。"
    "回答时尽量依据资料，并说明答案来自哪些片段。"
)


def answer(question: str, contexts: list[str]) -> str:
    if not contexts:
        return "资料中未找到相关内容。"

    context_text = "\n\n---\n\n".join(contexts)

    user_prompt = (
        f"资料：\n{context_text}\n\n"
        f"问题：{question}"
    )

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""