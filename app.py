
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="환영합니다!",
    page_icon="🐉",
    layout="wide"
)

# 디자인 설정
st.markdown("""
<style>
.stApp {
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

/* 버튼 글씨색 검정색 강제 적용 */
.stButton > button,
.stButton > button p,
.stButton > button span,
.stButton > button div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border: 2px solid #FFFFFF !important;
    border-radius: 12px !important;
    font-size: 20px !important;
    font-weight: bold !important;
}

.stButton > button:hover {
    background-color: #DDDDDD !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

.stButton > button:hover p,
.stButton > button:hover span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

h1, h2, p {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

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
        margin-top:50px;
        color:white;
        font-size:48px;">
        환영합니다! 🎉
    </h1>
    """, unsafe_allow_html=True)

    # 폭죽 효과
    st.balloons()

    # 용과 독수리 애니메이션
    components.html("""
    <div class="scene">

        <div class="dragon">🐉</div>

        <div class="fire">🔥🔥🔥</div>

        <div class="eagle">🦅</div>

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
        height: 450px;
        background: black;
        overflow: hidden;
    }

    /* 용 애니메이션 */
    .dragon {
        position: absolute;
        font-size: 115px;
        top: 70px;
        left: -180px;
        animation: dragonMove 5s ease-in-out forwards;
        z-index: 2;
    }

    @keyframes dragonMove {
        0% { left: -180px; }
        30% { left: 35%; }
        65% { left: 35%; }
        100% { left: 120%; }
    }

    /* 불 뿜기 */
    .fire {
        position: absolute;
        font-size: 45px;
        top: 145px;
        left: 40%;
        opacity: 0;
        animation: fireBreath 5s ease-in-out forwards;
        z-index: 3;
    }

    @keyframes fireBreath {
        0%, 30% {
            opacity: 0;
            transform: scale(0.2);
        }
        40%, 65% {
            opacity: 1;
            transform: scale(1.8);
        }
        80%, 100% {
            opacity: 0;
            transform: scale(0.2);
        }
    }

    /* 독수리 애니메이션 */
    .eagle {
        position: absolute;
        font-size: 85px;
        top: 220px;
        left: -130px;
        animation: eagleFly 6s linear 1s forwards;
        z-index: 4;
    }

    @keyframes eagleFly {
        0% {
            left: -130px;
            top: 250px;
            transform: rotate(-10deg) scale(0.8);
        }

        25% {
            top: 180px;
            transform: rotate(5deg) scale(1);
        }

        50% {
            top: 220px;
            transform: rotate(-5deg) scale(1.1);
        }

        75% {
            top: 130px;
            transform: rotate(5deg) scale(1);
        }

        100% {
            left: 120%;
            top: 180px;
            transform: rotate(0deg) scale(0.8);
        }
    }

    /* 환영 메시지 */
    .message {
        position: absolute;
        color: gold;
        font-size: 35px;
        font-weight: bold;
        top: 350px;
        width: 100%;
        text-align: center;
        opacity: 0;
        animation: messageShow 5s ease forwards;
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
    """, height=470)

    st.markdown("""
    <p style="
        text-align:center;
        color:gold;
        font-size:22px;">
        🐉 용과 🦅 독수리가 환영합니다!
    </p>
    """, unsafe_allow_html=True)

    if st.button("처음으로 돌아가기"):
        st.session_state.entered = False
        st.rerun()
