
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="환영합니다",
    page_icon="🎉",
    layout="centered"
)

# 검은색 배경 및 흰색 글씨
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

h1, h2, h3, p, label {
    color: #FFFFFF !important;
}

.stButton button {
    background-color: #FFFFFF;
    color: #000000;
    border-radius: 12px;
    border: none;
    padding: 12px 35px;
    font-size: 20px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #CCCCCC;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

# 화면 중앙 정렬
st.markdown(
    "<h1 style='text-align:center; margin-top:150px;'>WELCOME</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>버튼을 눌러 입장해 주세요.</p>",
    unsafe_allow_html=True
)

# 버튼
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    enter = st.button("들어가기", use_container_width=True)

# 버튼 클릭 이벤트
if enter:
    st.markdown(
        """
        <h1 style='text-align:center; margin-top:50px;'>
            환영합니다! 🎉
        </h1>
        """,
        unsafe_allow_html=True
    )

    # 폭죽 효과
    st.balloons()
    st.snow()
