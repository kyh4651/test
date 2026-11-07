
import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="가위바위보 게임",
    page_icon="🐉",
    layout="wide"
)

# -------------------------
# 디자인
# -------------------------

st.markdown("""
<style>
.stApp {
    background-color: #000000 !important;
    color: white !important;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stButton > button,
.stButton > button p,
.stButton > button span,
.stButton > button div {
    background-color: white !important;
    color: black !important;
    -webkit-text-fill-color: black !important;
    border: 2px solid white !important;
    border-radius: 12px !important;
    font-size: 20px !important;
    font-weight: bold !important;
    padding: 10px !important;
}

.stButton > button:hover {
    background-color: #dddddd !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 화면 상태
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "losses" not in st.session_state:
    st.session_state.losses = 0

if "draws" not in st.session_state:
    st.session_state.draws = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# =================================================
# 1. 처음 화면
# =================================================

if st.session_state.page == "home":

    st.markdown("""
    <h1 style="text-align:center; margin-top:150px;">
        WELCOME 🐉
    </h1>
    <p style="text-align:center; font-size:20px;">
        환영합니다! 입장해 주세요.
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("들어가기", use_container_width=True):
            st.session_state.page = "welcome"
            st.rerun()


# =================================================
# 2. 환영 화면
# =================================================

elif st.session_state.page == "welcome":

    st.markdown("""
    <h1 style="
        text-align:center;
        margin-top:50px;
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
        height: 350px;
        background: black;
        overflow: hidden;
    }

    .dragon {
        position: absolute;
        font-size: 110px;
        top: 40px;
        left: -180px;
        animation: dragonMove 5s ease-in-out forwards;
    }

    @keyframes dragonMove {
        0% { left: -180px; }
        30% { left: 35%; }
        65% { left: 35%; }
        100% { left: 120%; }
    }

    .fire {
        position: absolute;
        font-size: 45px;
        top: 110px;
        left: 40%;
        opacity: 0;
        animation: fireBreath 5s ease-in-out forwards;
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
        }
    }

    .eagle {
        position: absolute;
        font-size: 85px;
        top: 200px;
        left: -130px;
        animation: eagleFly 6s linear 1s forwards;
    }

    @keyframes eagleFly {
        0% {
            left: -130px;
            top: 220px;
        }
        50% {
            top: 100px;
        }
        100% {
            left: 120%;
            top: 160px;
        }
    }
    </style>
    """, height=370)

    st.markdown("""
    <h2 style="text-align:center; color:gold;">
        🐉 용과 🦅 독수리가 환영합니다!
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center; font-size:18px;">
        준비되셨나요? 가위바위보 게임을 시작해 보세요!
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("✊ 가위바위보", use_container_width=True):
            st.session_state.page = "game"
            st.rerun()


# =================================================
# 3. 가위바위보 게임 화면
# =================================================

elif st.session_state.page == "game":

    st.markdown("""
    <h1 style="text-align:center; margin-top:40px;">
        ✊ 가위바위보 게임 ✌️
    </h1>
    <p style="text-align:center; font-size:18px;">
        가위, 바위, 보 중 하나를 선택하세요!
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        "<h3 style='text-align:center;'>나의 선택</h3>",
        unsafe_allow_html=True
    )

    choices = {
        "가위": "✌️",
        "바위": "✊",
        "보": "✋"
    }

    col1, col2, col3 = st.columns(3)

    user_choice = None

    with col1:
        if st.button("✌️ 가위", use_container_width=True):
            user_choice = "가위"

    with col2:
        if st.button("✊ 바위", use_container_width=True):
            user_choice = "바위"

    with col3:
        if st.button("✋ 보", use_container_width=True):
            user_choice = "보"

    # 게임 진행
    if user_choice is not None:

        computer_choice = random.choice(
            ["가위", "바위", "보"]
        )

        if user_choice == computer_choice:
            result = "무승부"
            st.session_state.draws += 1

        elif (
            (user_choice == "가위" and computer_choice == "보")
            or
            (user_choice == "바위" and computer_choice == "가위")
            or
            (user_choice == "보" and computer_choice == "바위")
        ):
            result = "승리!"
            st.session_state.wins += 1

        else:
            result = "패배!"
            st.session_state.losses += 1

        st.session_state.last_result = {
            "user": user_choice,
            "computer": computer_choice,
            "result": result
        }

        st.rerun()

    # 결과 표시
    if st.session_state.last_result:

        data = st.session_state.last_result

        st.markdown("---")

        st.markdown(
            "<h2 style='text-align:center;'>🎮 게임 결과</h2>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                "<p style='text-align:center;'>나의 선택</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<h1 style='text-align:center;'>"
                f"{choices[data['user']]}</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<h3 style='text-align:center;'>"
                f"{data['user']}</h3>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                "<p style='text-align:center;'>컴퓨터의 선택</p>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<h1 style='text-align:center;'>"
                f"{choices[data['computer']]}</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<h3 style='text-align:center;'>"
                f"{data['computer']}</h3>",
                unsafe_allow_html=True
            )

        if data["result"] == "승리!":
            st.success("🎉 축하합니다! 당신이 이겼습니다!")
            st.balloons()

        elif data["result"] == "패배!":
            st.error("😢 컴퓨터가 이겼습니다!")

        else:
            st.info("🤝 비겼습니다!")

        st.markdown(
            f"<h1 style='text-align:center;'>{data['result']}</h1>",
            unsafe_allow_html=True
        )

    # 누적 전적
    st.markdown("---")

    st.markdown(
        "<h2 style='text-align:center;'>📊 나의 누적 전적</h2>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏆 승리", st.session_state.wins)

    with col2:
        st.metric("💀 패배", st.session_state.losses)

    with col3:
        st.metric("🤝 무승부", st.session_state.draws)

    total = (
        st.session_state.wins
        + st.session_state.losses
        + st.session_state.draws
    )

    if total > 0:
        win_rate = st.session_state.wins / total * 100
        st.markdown(
            f"<h3 style='text-align:center;'>승률: {win_rate:.1f}%</h3>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 전적 초기화", use_container_width=True):
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.session_state.draws = 0
            st.session_state.last_result = None
            st.rerun()

    with col2:
        if st.button("🏠 환영 화면으로", use_container_width=True):
            st.session_state.page = "welcome"
            st.session_state.last_result = None
            st.rerun()
