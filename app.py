
import streamlit as st
import datetime
import random
import io
import wave
import math
import struct

KST = datetime.timezone(datetime.timedelta(hours=9))

st.set_page_config(
    page_title="수학 알람",
    page_icon="⏰",
    layout="centered"
)

# -------------------------
# 세션 데이터
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "list"

if "alarms" not in st.session_state:
    st.session_state.alarms = []

if "active_alarm" not in st.session_state:
    st.session_state.active_alarm = None

if "notice" not in st.session_state:
    st.session_state.notice = ""

if "problem" not in st.session_state:
    st.session_state.problem = None


# -------------------------
# 화면 디자인
# -------------------------

def apply_design(dark=False):
    if dark:
        background = "#000000"
        foreground = "#FFFFFF"
    else:
        background = "#FFFFFF"
        foreground = "#111111"

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {background};
        color: {foreground};
    }}

    h1, h2, h3, p, label {{
        color: {foreground} !important;
    }}

    div.stButton > button {{
        border-radius: 12px;
        height: 48px;
        font-weight: bold;
    }}

    div[data-testid="stNumberInput"] input {{
        font-size: 24px;
        text-align: center;
    }}

    </style>
    """, unsafe_allow_html=True)


# -------------------------
# 공통수학2 문제 생성
# -------------------------

def generate_problem():
    problem_type = random.choice([
        "distance",
        "midpoint",
        "slope",
        "circle",
        "set_union",
        "set_difference",
        "function",
        "composition"
    ])

    if problem_type == "distance":
        pairs = [(3, 4), (5, 12), (8, 15), (7, 24)]
        dx, dy = random.choice(pairs)

        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)

        x2 = x1 + dx
        y2 = y1 + dy

        answer = int(math.sqrt(dx**2 + dy**2))

        question = (
            f"두 점 A({x1}, {y1}), B({x2}, {y2}) 사이의 "
            f"거리를 구하시오."
        )

    elif problem_type == "midpoint":
        x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
        x2, y2 = random.randint(-8, 8), random.randint(-8, 8)

        answer = x1 + x2

        question = (
            f"두 점 A({x1}, {y1}), B({x2}, {y2})의 "
            f"중점의 x좌표를 구하시오."
        )
        answer = (x1 + x2) // 2

    elif problem_type == "slope":
        x1 = random.randint(-5, 5)
        y1 = random.randint(-5, 5)
        dx = random.choice([-4, -3, -2, 2, 3, 4])
        dy = random.choice([-6, -4, -2, 2, 4, 6])

        x2 = x1 + dx
        y2 = y1 + dy

        # 정수 기울기가 되도록 조정
        dy = random.choice([-3, -2, -1, 1, 2, 3]) * dx
        y2 = y1 + dy

        answer = dy // dx

        question = (
            f"두 점 A({x1}, {y1}), B({x2}, {y2})를 "
            f"지나는 직선의 기울기를 구하시오."
        )

    elif problem_type == "circle":
        radius = random.randint(2, 12)
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)

        question = (
            f"원의 방정식이 "
            f"(x - ({a}))² + (y - ({b}))² = {radius**2}일 때, "
            f"원의 반지름을 구하시오."
        )
        answer = radius

    elif problem_type == "set_union":
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        common = random.randint(1, min(a, b) - 1)

        answer = a + b - common

        question = (
            f"두 집합 A, B에 대하여 n(A)={a}, "
            f"n(B)={b}, n(A∩B)={common}이다. "
            f"n(A∪B)를 구하시오."
        )

    elif problem_type == "set_difference":
        a = random.randint(5, 15)
        common = random.randint(1, a - 1)

        answer = a - common

        question = (
            f"두 집합 A, B에 대하여 n(A)={a}, "
            f"n(A∩B)={common}이다. "
            f"n(A-B)를 구하시오."
        )

    elif problem_type == "function":
        a = random.randint(-5, 5)
        if a == 0:
            a = 2

        b = random.randint(-10, 10)
        x = random.randint(-5, 5)

        answer = a * x + b

        question = (
            f"함수 f(x)={a}x+({b})에 대하여 "
            f"f({x})의 값을 구하시오."
        )

    else:
        a = random.randint(1, 5)
        b = random.randint(-5, 5)
        c = random.randint(1, 5)
        d = random.randint(-5, 5)
        x = random.randint(-3, 3)

        answer = a * (c * x + d) + b

        question = (
            f"f(x)={a}x+({b}), g(x)={c}x+({d})일 때, "
            f"(f∘g)({x})의 값을 구하시오."
        )

    return {
        "question": question,
        "answer": int(answer)
    }


# -------------------------
# 일정한 반복 알람 소리
# -------------------------

@st.cache_data
def make_alarm_sound():
    sample_rate = 44100
    duration = 2
    frequency = 660
    volume = 0.35

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = []

        for i in range(sample_rate * duration):
            value = int(
                32767 * volume *
                math.sin(2 * math.pi * frequency * i / sample_rate)
            )
            frames.append(struct.pack("<h", value))

        wav.writeframes(b"".join(frames))

    return buffer.getvalue()


# -------------------------
# 알람 시간 확인
# -------------------------

@st.fragment(run_every="1s")
def alarm_checker():
    if st.session_state.active_alarm is not None:
        return

    now = datetime.datetime.now(KST)

    for alarm in st.session_state.alarms:
        if alarm["target"] <= now:
            st.session_state.active_alarm = alarm
            st.session_state.problem = (
                generate_problem() if alarm["math"] else None
            )
            st.rerun()


# -------------------------
# 알람 목록 화면
# -------------------------

def list_screen():
    apply_design(False)

    st.title("⏰ 알람")

    if st.session_state.notice:
        st.success(st.session_state.notice)
        st.session_state.notice = ""

    if st.button("＋ 알람 추가", use_container_width=True):
        st.session_state.page = "add"
        st.rerun()

    st.divider()

    if not st.session_state.alarms:
        st.info("설정된 알람이 없습니다.")

    for alarm in st.session_state.alarms:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.subheader(alarm["display"])
            if alarm["math"]:
                st.caption("공통수학2 문제 알람")
            else:
                st.caption("일반 알람")

        with col2:
            st.write("")
            if st.button("삭제", key=alarm["id"]):
                st.session_state.alarms.remove(alarm)
                st.rerun()

        st.divider()


# -------------------------
# 알람 추가 화면
# -------------------------

def add_screen():
    apply_design(True)

    st.title("알람 추가")

    period = st.radio(
        "오전 / 오후",
        ["오전", "오후"],
        horizontal=True
    )

    col1, col2 = st.columns(2)

    with col1:
        hour = st.selectbox(
            "시",
            list(range(1, 13)),
            index=8
        )

    with col2:
        minute = st.selectbox(
            "분",
            list(range(60)),
            index=0,
            format_func=lambda x: f"{x:02d}"
        )

    st.divider()

    math_enabled = st.toggle(
        "수학 문제 사용",
        value=True
    )

    level = "공통수학2"

    if math_enabled:
        st.markdown("### 문제 범위")
        st.markdown("**고등학교 1학년 공통수학2**")
        st.caption(
            "도형의 방정식 · 집합과 명제 · 함수와 그래프"
        )

    st.write("")

    if st.button("저장", use_container_width=True):
        hour24 = hour % 12

        if period == "오후":
            hour24 += 12

        now = datetime.datetime.now(KST)

        target = now.replace(
            hour=hour24,
            minute=minute,
            second=0,
            microsecond=0
        )

        if target <= now:
            target += datetime.timedelta(days=1)

        alarm = {
            "id": str(random.random()),
            "target": target,
            "display": f"{period} {hour}시 {minute:02d}분",
            "math": math_enabled
        }

        st.session_state.alarms.append(alarm)

        st.session_state.page = "list"
        st.session_state.notice = "알람이 저장되었습니다."
        st.rerun()

    if st.button("취소", use_container_width=True):
        st.session_state.page = "list"
        st.rerun()


# -------------------------
# 알람이 울리는 화면
# -------------------------

def ringing_screen():
    apply_design(False)

    alarm = st.session_state.active_alarm

    st.title("⏰ 알람이 울립니다!")

    now = datetime.datetime.now(KST)

    st.markdown(
        f"<h2 style='text-align:center'>{now.strftime('%H:%M:%S')}</h2>",
        unsafe_allow_html=True
    )

    # 반복 재생되는 일정한 알람음
    st.audio(
        make_alarm_sound(),
        format="audio/wav",
        autoplay=True,
        loop=True
    )

    st.divider()

    if alarm["math"]:
        problem = st.session_state.problem

        st.markdown(
            "<h2 style='text-align:center'>공통수학2 문제</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h3 style='text-align:center'>{problem['question']}</h3>",
            unsafe_allow_html=True
        )

        st.write("")

        with st.form("answer_form"):
            answer = st.number_input(
                "정답을 입력하세요",
                step=1,
                value=0
            )

            submitted = st.form_submit_button(
                "정답 확인",
                use_container_width=True
            )

        if submitted:
            if int(answer) == problem["answer"]:
                st.session_state.alarms = [
                    a for a in st.session_state.alarms
                    if a["id"] != alarm["id"]
                ]

                st.session_state.active_alarm = None
                st.session_state.problem = None
                st.session_state.page = "list"
                st.session_state.notice = "정답입니다! 알람이 꺼졌습니다."
                st.rerun()
            else:
                st.error("틀렸습니다. 다시 풀어보세요!")

    else:
        st.subheader("알람이 울리고 있습니다.")

        if st.button("알람 끄기", use_container_width=True):
            st.session_state.alarms = [
                a for a in st.session_state.alarms
                if a["id"] != alarm["id"]
            ]

            st.session_state.active_alarm = None
            st.session_state.page = "list"
            st.session_state.notice = "알람이 꺼졌습니다."
            st.rerun()


# -------------------------
# 앱 실행
# -------------------------

alarm_checker()

if st.session_state.active_alarm is not None:
    ringing_screen()

elif st.session_state.page == "add":
    add_screen()

else:
    list_screen()
