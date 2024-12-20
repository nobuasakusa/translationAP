import streamlit as st
import openai
from dotenv import load_dotenv
import os
import requests

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# 翻訳を行う関数
def translate_text(input_text, source_lang, target_lang):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": f"You are a translation assistant."},
                {"role": "user", "content": f"Translate this text from {source_lang} to {target_lang}: {input_text}"},
            ],
            "max_tokens_to_sample": 1000,
            "temperature": 0
        }
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response_data = response.json()
        if response.status_code == 200:
            return response_data["completion"].strip()
        else:
            return f"Error: {response_data.get('error', 'Unknown error')}"
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlitアプリ
st.title("翻訳アプリケーション")
st.write("右側の枠に原文を入力すると、左側の枠に翻訳結果が表示されます。")

# タブを作成
tabs = st.tabs(["日本語 → 英語", "英語 → 日本語"])

# 日本語 → 英語
tab1 = tabs[0]
with tab1:
    st.header("日本語 → 英語")
    input_text_ja_en = st.text_area("原文を入力してください:", key="ja_en_input")
    if st.button("翻訳", key="translate_ja_en"):
        if input_text_ja_en.strip():
            translated_text = translate_text(input_text_ja_en, "Japanese", "English")
            st.text_area("翻訳結果:", translated_text, key="ja_en_output", height=200)
        else:
            st.warning("原文を入力してください。")

# 英語 → 日本語
tab2 = tabs[1]
with tab2:
    st.header("英語 → 日本語")
    input_text_en_ja = st.text_area("Enter the text to translate:", key="en_ja_input")
    if st.button("Translate", key="translate_en_ja"):
        if input_text_en_ja.strip():
            translated_text = translate_text(input_text_en_ja, "English", "Japanese")
            st.text_area("翻訳結果:", translated_text, key="en_ja_output", height=200)
        else:
            st.warning("Please enter text to translate.")
