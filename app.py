import os
from openai import OpenAI
import gradio as gr

client = OpenAI()

SYSTEM_PROMPT = """
너는 한국 대학생을 돕는 공부 계획 코치야.
현실적으로 지킬 수 있는, 무리하지 않는 계획을 세워줘.
휴식/복습도 포함해줘.
"""

def make_plan(subjects, hours_per_day, weeks, detail_level, extra_info):
    if not subjects.strip():
        return "먼저 공부할 과목/주제를 적어줘!"

    user_prompt = f"""
    아래 정보를 바탕으로 공부 계획을 짜줘.

    1. 공부할 과목/주제:
    {subjects}

    2. 하루 공부 가능 시간: {hours_per_day}시간

    3. 총 기간: {weeks}주

    4. 상세 정도: {detail_level}
       - '간단하게': 주차별 큰 흐름 위주
       - '적당히': 주차별 + 간단한 요일 분배
       - '상세하게': 요일별로 할 일을 꽤 구체적으로

    5. 추가 정보:
    {extra_info}

    출력 형식:
    [전체 전략]
    - 4~6줄 정도로 공부 방향 설명

    [주차별 계획]
    1주차:
      - 월: ...
      - 화: ...
      - ...

    최대한 현실적으로, 과도한 계획 말고
    복습/휴식도 일정에 포함해 줘.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 있으면 gpt-4o 써도 좋고
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",  "content": user_prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # 에러 메시지를 그대로 보여주면 디버깅에 도움됨
        return f"에러 발생: {e}"


with gr.Blocks() as demo:
    gr.Markdown("# 📚 공부 플랜 짜주는 AI (Jupyter 버전)")

    subjects = gr.Textbox(
        label="공부할 과목/주제",
        placeholder="예: 통계학, 선형대수, 파이썬 프로그래밍",
        lines=2,
    )
    hours = gr.Slider(
        minimum=1, maximum=10, value=2, step=0.5,
        label="하루 공부 시간(시간)"
    )
    weeks = gr.Slider(
        minimum=1, maximum=12, value=3, step=1,
        label="기간(주)"
    )

    detail = gr.Radio(
        ["간단하게", "적당히", "상세하게"],
        value="적당히",
        label="계획 상세 정도"
    )

    extra = gr.Textbox(
        label="추가 정보 (선택)",
        placeholder="예: 3주 뒤 통계학 중간고사, 주말엔 3시간 이상 못 함 등",
        lines=3,
    )

    output = gr.Textbox(
        label="AI가 만든 공부 계획",
        lines=20
    )

    btn = gr.Button("공부 플랜 생성하기 🚀")
    btn.click(
        fn=make_plan,
        inputs=[subjects, hours, weeks, detail, extra],
        outputs=output
    )

demo.launch(inline=True)
