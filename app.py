"""
스펙노트 (SpecNote) — Streamlit Cloud 배포용 래퍼

이 앱은 완전히 클라이언트 사이드(HTML/CSS/JS)로 동작하는 index.html을
Streamlit 페이지 안에 그대로 임베드합니다.
- PDF 텍스트 추출: 브라우저에서 pdf.js(CDN)로 처리 (서버 전송 없음)
- AI 보완 추출: 사용자가 입력한 Anthropic API 키로 브라우저가 직접
  https://api.anthropic.com 을 호출 (Streamlit 서버는 관여하지 않음)

따라서 이 app.py에는 별도의 백엔드 로직이 없고, index.html을 읽어서
components.v1.html로 렌더링하는 역할만 합니다.
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="스펙노트 (SpecNote) — 원료 스펙 관리",
    page_icon="🧪",
    layout="wide",
)

# app.py와 같은 폴더에 있는 index.html을 읽어온다.
HTML_PATH = Path(__file__).parent / "index.html"

if not HTML_PATH.exists():
    st.error(
        "index.html 파일을 찾을 수 없습니다. "
        "app.py와 같은 폴더에 index.html을 함께 업로드해주세요."
    )
    st.stop()

html_content = HTML_PATH.read_text(encoding="utf-8")

# 사이드바: iframe 높이 조절 (표에 행이 많아지면 늘려서 사용)
with st.sidebar:
    st.markdown("### ⚙️ 화면 설정")
    height = st.slider(
        "표시 영역 높이 (px)",
        min_value=800,
        max_value=3000,
        value=1500,
        step=100,
        help="원료 목록이 많아 표가 길어지면 높이를 늘려주세요.",
    )
    st.caption(
        "이 앱은 PDF 파싱과 AI 보완 추출을 모두 브라우저에서 직접 처리합니다. "
        "Anthropic API 키를 입력하면 브라우저가 api.anthropic.com을 직접 호출하며, "
        "Streamlit 서버로는 전송되지 않습니다. (프로토타입 용도 — 실서비스에는 "
        "백엔드 프록시를 두는 것을 권장합니다.)"
    )

components.html(html_content, height=height, scrolling=True)
