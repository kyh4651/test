
import streamlit as st
import datetime
import random
import io
import wave
import math
import struct
import uuid

# -------------------------
# 기본 설정
# -------------------------

st.set_page_config(
    page_title="수학 알람",
    page_icon="⏰",
    layout="centered"
)

KST = datetime.timezone(datetime.timedelta(hours=9))

SCOPES = [
    "공통수학1",
    "공통수학2",
    "대수",
    "미적분Ⅰ",
    "확률과 통계",
    "기하",
    "미적분Ⅱ"
]

LEVELS = ["하", "중", "상"]


# -------------------------
# 세션 데이터 초기화
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
# 디자인
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

    h1, h2, h3, h4, p, label {{
        color: {foreground} !important;
    }}

    /* 모든 버튼의 글자색 검은색 */
    div.stButton > button,
    div.stButton > button p,
    div.stFormSubmitButton > button,
    div.stFormSubmitButton > button p,
    button[kind] {{
        color: #000000 !important;
        font-weight: bold !important;
    }}

    div.stButton > button,
    div.stFormSubmitButton > button {{
        border-radius: 12px;
        min-height: 48px;
    }}

    div[data-testid="stNumberInput"] input {{
        font-size: 24px;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)


# -------------------------
# 난이도별 범위 설정
# -------------------------

def get_numbers(level):

    if level == "하":
        return 2, 5

    elif level == "중":
        return 5, 10

    else:
        return 10, 20


# -------------------------
# 수학 문제 생성
# -------------------------

def generate_problem(scope, level):

    low, high = get_numbers(level)

    # 공통수학1
    if scope == "공통수학1":

        a = random.randint(1, high)
        b = random.randint(-high, high)
        c = random.randint(-high, high)
        x = random.randint(-low, low)

        answer = a * x**2 + b * x + c

        question = (
            f"다항식 f(x)={a}x²+({b})x+({c})에 대하여 "
            f"f({x})의 값을 구하시오."
        )

    # 공통수학2
    elif scope == "공통수학2":

        kind = random.choice(["distance", "circle", "set"])

        if kind == "distance":

            dx = random.choice([3, 4, 5, 6, 8])
            dy = random.choice([4, 5, 6, 8, 15])

            if level == "하":
                dx, dy = 3, 4
            elif level == "중":
                dx, dy = 5, 12
            else:
                dx, dy = 8, 15

            x1 = random.randint(-5, 5)
            y1 = random.randint(-5, 5)

            x2 = x1 + dx
            y2 = y1 + dy

            answer = int(math.sqrt(dx**2 + dy**2))

            question = (
                f"두 점 A({x1}, {y1}), B({x2}, {y2}) 사이의 "
                f"거리를 구하시오."
            )

        elif kind == "circle":

            radius = random.randint(low, high)
            a = random.randint(-5, 5)
            b = random.randint(-5, 5)

            answer = radius

            question = (
                f"원의 방정식이 "
                f"(x-({a}))²+(y-({b}))²={radius**2}일 때, "
                f"반지름을 구하시오."
            )

        else:

            a = random.randint(high, high + 10)
            b = random.randint(high, high + 10)
            common = random.randint(1, min(a, b) - 1)

            answer = a + b - common

            question = (
                f"n(A)={a}, n(B)={b}, n(A∩B)={common}일 때, "
                f"n(A∪B)를 구하시오."
            )

    # 대수
    elif scope == "대수":

        if level == "하":
            base = random.choice([2, 3])
            exponent = random.randint(2, 4)

        elif level == "중":
            base = random.choice([2, 3, 5])
            exponent = random.randint(3, 6)

        else:
            base = random.choice([2, 3, 5])
            exponent = random.randint(5, 8)

        kind = random.choice(["exponential", "logarithm"])

        if kind == "exponential":

            answer = base ** exponent

            question = (
                f"{base}^{exponent}의 값을 구하시오."
            )

        else:

            answer = exponent

            question = (
                f"log_{base}({base**exponent})의 값을 구하시오."
            )

    # 미적분Ⅰ
    elif scope == "미적분Ⅰ":

        a = random.randint(1, high)
        b = random.randint(-high, high)
        c = random.randint(-high, high)
        x = random.randint(-low, low)

        answer = 2 * a * x + b

        question = (
            f"함수 f(x)={a}x²+({b})x+({c})에 대하여 "
            f"f'({x})의 값을 구하시오."
        )

        if level == "상":

            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            x = random.randint(-5, 5)

            answer = 3 * a * x**2 + 2 * b * x + c

            question = (
                f"함수 f(x)={a}x³+({b})x²+({c})x에 대하여 "
                f"f'({x})의 값을 구하시오."
            )

    # 확률과 통계
    elif scope == "확률과 통계":

        if level == "하":

            n = random.randint(4, 7)
            r = 2

        elif level == "중":

            n = random.randint(7, 10)
            r = random.randint(2, 4)

        else:

            n = random.randint(10, 15)
            r = random.randint(3, 6)

        answer = math.comb(n, r)

        question = (
            f"서로 다른 {n}개 중에서 {r}개를 선택하는 "
            f"경우의 수를 구하시오."
        )

    # 기하
    elif scope == "기하":

        if level == "하":
            x1, y1 = 1, 2
            x2, y2 = 3, 4

        elif level == "중":
            x1 = random.randint(2, 8)
            y1 = random.randint(2, 8)
            x2 = random.randint(2, 8)
            y2 = random.randint(2, 8)

        else:
            x1 = random.randint(-10, 10)
            y1 = random.randint(-10, 10)
            x2 = random.randint(-10, 10)
            y2 = random.randint(-10, 10)

        answer = x1 * x2 + y1 * y2

        question = (
            f"두 벡터 a=({x1}, {y1}), b=({x2}, {y2})에 대하여 "
            f"a·b의 값을 구하시오."
        )

    # 미적분Ⅱ
    elif scope == "미적분Ⅱ":

        if level == "하":

            n = random.randint(2, 4)
            x = 1
            a = random.randint(1, 5)

            answer = a * n

            question = (
                f"함수 f(x)={a}x^{n}에 대하여 "
                f"f'(1)의 값을 구하시오."
            )

        elif level == "중":

            n = random.randint(3, 5)
            a = random.randint(1, 5)
            x = random.randint(1, 3)

            answer = a * n * x**(n - 1)

            question = (
                f"함수 f(x)={a}x^{n}에 대하여 "
                f"f'({x})의 값을 구하시오."
            )

        else:

            a = random.randint(1, 4)
            b = random.randint(1, 4)
            x = random.randint(1, 3)

            answer = 3 * a * x**2 + 2 * b * x

            question = (
                f"함수 f(x)={a}x³+{b}x²에 대하여 "
                f"f'({x})의 값을 구하시오."
            )

    else:

        question = "문제를 생성할 수 없습니다."
        answer = 0

    return {
        "question": question,
        "answer": int(answer),
        "scope": scope,
        "level": level
    }


# -------------------------
# 알람 소리
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
                math.sin(
                    2 * math.pi * frequency * i / sample_rate
                )
            )

            frames.append(struct.pack("<h", value))

        wav.writeframes(b"".join(frames))

    return buffer.getvalue()


# -------------------------
# 알람 시간 변환
# -------------------------

def normalize_target(target):

    if isinstance(target, str):
        try:
            target = datetime.datetime.fromisoformat(target)
        except ValueError:
            return None

    if not isinstance(target, datetime.datetime):
        return None

    if target.tzinfo is None:
        target = target.replace(tzinfo=KST)
    else:
        target = target.astimezone(KST)

    return target


# -------------------------
# 알람 시간 확인
# -------------------------

@st.fragment(run_every="1s")
def alarm_checker():

    if st.session_state.active_alarm is not None:
        return

    now = datetime.datetime.now(KST)

    for alarm in st.session_state.alarms:

        target = normalize_target(alarm.get("target"))

        if target is None:
            continue

        alarm["target"] = target

        if target <= now:

            st.session_state.active_alarm = alarm

            if alarm.get("math", False):

                scope = alarm.get("scope", "공통수학2")
                level = alarm.get("level", "중")

                st.session_state.problem = generate_problem(
                    scope,
                    level
                )

            else:

                st.session_state.problem = None

            st.rerun()
            return


# -------------------------
# 알람 목록
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

            if alarm.get("math", False):

                st.caption(
                    f"{alarm.get('scope', '공통수학2')} "
                    f"· 난이도 {alarm.get('level', '중')}"
                )

            else:

                st.caption("일반 알람")

        with col2:

            st.write("")

            if st.button("삭제", key=alarm["id"]):

                st.session_state.alarms.remove(alarm)
                st.rerun()

        st.divider()


# -------------------------
# 알람 추가
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

    if math_enabled:

        st.markdown("### 문제 범위")

        scope = st.selectbox(
            "고등학교 수학 과목 선택",
            SCOPES,
            index=1
        )

        st.markdown("### 문제 난이도")

        level = st.radio(
            "난이도 선택",
            LEVELS,
            horizontal=True,
            index=1
        )

    else:

        scope = "공통수학2"
        level = "중"

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
            "id": str(uuid.uuid4()),
            "target": target,
            "display": f"{period} {hour}시 {minute:02d}분",
            "math": math_enabled,
            "scope": scope,
            "level": level
        }

        st.session_state.alarms.append(alarm)

        st.session_state.page = "list"
        st.session_state.notice = "알람이 저장되었습니다."

        st.rerun()

    if st.button("취소", use_container_width=True):

        st.session_state.page = "list"
        st.rerun()


# -------------------------
# 알람 실행
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

    st.audio(
        make_alarm_sound(),
        format="audio/wav",
        autoplay=True,
        loop=True
    )

    st.divider()

    if alarm.get("math", False):

        problem = st.session_state.problem

        st.markdown(
            f"<h3 style='text-align:center'>{problem['scope']} 문제</h3>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p style='text-align:center'>난이도: {problem['level']}</p>",
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

                st.session_state.notice = (
                    "정답입니다! 알람이 꺼졌습니다."
                )

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
