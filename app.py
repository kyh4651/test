
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="환영합니다!",
    page_icon="🐉",
    layout="wide"
)

# 검은색 배경 및 흰색 글씨
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}

h1, h2, p {
    color: white !important;
}

.stButton button {
    background-color: white !important;
    color: black !important;
    border: 2px solid white !important;
    border-radius: 12px !important;
    font-size: 22px !important;
    font-weight: bold !important;
    padding: 12px 30px !important;
}

.stButton button:hover {
    background-color: #dddddd !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# 세션 상태
if "entered" not in st.session_state:
    st.session_state.entered = False

# 첫 화면
if not st.session_state.entered:

    st.markdown("""
    <h1 style="text-align:center; margin-top:180px;">
        WELCOME
    </h1>
    <p style="text-align:center; font-size:20px;">
        버튼을 눌러 입장해 주세요.
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("들어가기", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

# 입장 후 화면
else:

    st.markdown("""
    <h1 style="
        text-align:center;
        margin-top:60px;
        color:white;
        font-size:48px;">
        환영합니다! 🎉
    </h1>
    """, unsafe_allow_html=True)

    # 폭죽 효과
    st.balloons()

    # 용 애니메이션
    components.html("""
    <div class="scene">
        <div class="dragon">🐉</div>
        <div class="fire">🔥🔥🔥</div>
        <div class="message">WELCOME!</div>
    </div>

    <style>
    body {
        background: black;
        margin: 0;
        overflow: hidden;
    }

    .scene {
        position: relative;
        width: 100%;
        height: 420px;
        background: black;
        overflow: hidden;
    }

    .dragon {
        position: absolute;
        font-size: 120px;
        top: 100px;
        left: -180px;
        animation: dragonMove 5s ease-in-out forwards;
        z-index: 2;
    }

    .fire {
        position: absolute;
        font-size: 45px;
        top: 170px;
        left: 40%;
        opacity: 0;
        animation: fireBreath 5s ease-in-out forwards;
        z-index: 3;
    }

    .message {
        position: absolute;
        color: gold;
        font-size: 35px;
        font-weight: bold;
        top: 300px;
        width: 100%;
        text-align: center;
        opacity: 0;
        animation: messageShow 5s ease forwards;
    }

    @keyframes dragonMove {
        0% {
            left: -180px;
            transform: scaleX(1);
        }
        30% {
            left: 35%;
            transform: scaleX(1);
        }
        65% {
            left: 35%;
            transform: scaleX(1);
        }
        100% {
            left: 120%;
            transform: scaleX(1);
        }
    }

    @keyframes fireBreath {
        0%, 30% {
            opacity: 0;
            transform: scale(0.2);
        }
        40% {
            opacity: 1;
            transform: scale(1.5);
        }
        65% {
            opacity: 1;
            transform: scale(1.8);
        }
        80%, 100% {
            opacity: 0;
            transform: scale(0.2);
        }
    }

    @keyframes messageShow {
        0%, 40% {
            opacity: 0;
            transform: scale(0.5);
        }
        60%, 85% {
            opacity: 1;
            transform: scale(1);
        }
        100% {
            opacity: 0;
        }
    }
    </style>
    """, height=440)

    st.markdown("""
    <p style="text-align:center; color:gold; font-size:20px;">
        🐉 전설의 용이 등장했습니다!
    </p>
    """, unsafe_allow_html=True)

    if st.button("처음으로 돌아가기"):
        st.session_state.entered = False
        st.rerun()
