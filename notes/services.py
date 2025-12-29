# notes/services.py
from openai import OpenAI

def summarize_korean(text: str) -> str:
    """
    긴 텍스트를 한국어로 깔끔하게 요약
    """
    client = OpenAI()  # OPENAI_API_KEY 환경변수 사용 :contentReference[oaicite:3]{index=3}

    # 너무 길면 비용/시간 커지니 서버에서 간단 컷(원하면 더 정교화 가능)
    text = (text or "").strip()
    if not text:
        return ""

    if len(text) > 12000:
        text = text[:12000]

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "너는 공부노트를 요약하는 도우미야. "
                    "출력은 한국어로, 불필요한 장식 없이 핵심만 정리해."
                ),
            },
            {
                "role": "user",
                "content": (
                    "아래 노트를 시험/복습에 유용하게 요약해줘.\n\n"
                    "요구 형식:\n"
                    "1) 한 줄 요약\n"
                    "2) 핵심 포인트 5개 (불릿)\n"
                    "3) 용어 정리 3개 (용어: 설명)\n\n"
                    f"노트 내용:\n{text}"
                ),
            },
        ],
    )
    return (response.output_text or "").strip()
