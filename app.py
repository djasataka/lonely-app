# -*- coding: utf-8 -*-

# ======================
# 1. import
# ======================
import streamlit as st
import os
from characters import CHARACTERS

# OpenAIを使う場合（後で有効化）
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except:
    client = None


# ======================
# 2. ページ設定
# ======================
st.set_page_config(
    page_title="高齢者おしゃべりアプリ",
    page_icon="🧓",
    layout="centered"
)

st.title("🧓 おしゃべり相手")
st.write("ゆっくり、安心してお話しください。")


# ======================
# 3. セッション初期化
# ======================
def init_session():
    if "role" not in st.session_state:
        st.session_state.role = "孫"
    if "messages" not in st.session_state:
        st.session_state.messages = []

init_session()


# ======================
# 4. UI（高齢者向け）
# ======================
def select_role():
    st.write("### 話し相手を選んでください")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👶 孫", use_container_width=True):
            st.session_state.role = "孫"

    with col2:
        if st.button("🤝 友人", use_container_width=True):
            st.session_state.role = "友人"

    with col3:
        if st.button("🎓 先生", use_container_width=True):
            st.session_state.role = "先生"

    st.write("#### 今のお相手")
    st.write(CHARACTERS[st.session_state.role]["description"])

select_role()


# ======================
# 5. AI応答処理
# ======================
def generate_reply(user_input):
    role = st.session_state.role

    # OpenAIが使える場合
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CHARACTERS[role]["system"]},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content
        except:
            pass

    # フォールバック（AI未接続でも動く）
    return f"{role}として、ゆっくり聞いていますよ。\n「{user_input}」"


# ======================
# 6. 入力と処理
# ======================
user_input = st.chat_input("今日はどんな一日でしたか？（短くても大丈夫です）")

if user_input:
    st.session_state.messages.append(("user", user_input))
    reply = generate_reply(user_input)
    st.session_state.messages.append(("assistant", reply))


# ======================
# 7. 表示
# ======================
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)
