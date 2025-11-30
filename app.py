import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


# .env を読み込む（OpenAI API Key を参照）
load_dotenv()

def run_llm(input_text: str, expert_type: str) -> str:
    """入力テキストと選択した専門家種別から LLM の回答を返す関数"""

    # 選択された専門家に応じて system メッセージを切り替える
    if expert_type == "AIプログラマー":
        system_prompt = "あなたは優秀なAIプログラマーです。専門知識を活かして要件に応えるプログラムを提供してください。"
    else:
        system_prompt = "あなたは経験豊富なITコンサルタントです。実務で効力を発揮するITシステムを提案してください。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    result = llm(messages)

    return result.content


# -------------------------
# Streamlit アプリ
# -------------------------
st.title("LLM機能を搭載したWebアプリ")

st.write("##### このアプリについて")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで 各専門家に問い合わせることができます。")
st.write("ラジオボタンで「AIプログラマー」か「ITコンサルティング」を選択してください。")
st.write("問い合わせたい内容を入力したうえで「実行」ボタンを押すと、LLMが回答を生成します。")

st.divider()

def reset_input():
    st.session_state["user_input"] = ""

# 専門家タイプ選択
selected_expert = st.radio(
    "専門家を選択してください。",
    ["AIプログラマー", "ITコンサルティング"],
    key="expert_select",
    on_change=reset_input
)

# 入力フォーム（1つ）
user_input = st.text_input(
    "問い合わせたい内容を入力してください。",
    key="user_input"
)

# 実行ボタン
if st.button("実行"):
    st.divider()

    if user_input:
        # 関数に「入力テキスト」と「ラジオボタンの選択値」を渡す
        response = run_llm(user_input, selected_expert)
        st.write("##### ▼ LLM からの回答")
        st.write(response)
    else:
        st.error("問い合わせ内容を入力してから「実行」ボタンを押してください。")
