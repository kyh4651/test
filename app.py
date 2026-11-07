
import streamlit as st
import datetime
import random
import uuid
import io
import wave
import math
import struct
import time

# ==========================================
# 1. 기본 설정
# ==========================================

st.set_page_config(
    page_title="수학 타이머",
    page_icon="⏰",
    layout="centered"
)

# ==========================================
# 2. 화면 디자인
# ==========================================

def apply_design(dark=False):

    if dark:
        background = "#111111"
        foreground = "#FFFFFF"
        input_background = "#292929"
    else:
        background = "#FFFFFF"
        foreground = "#111111"
        input_background = "#F5F5F5"

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {background};
        color: {foreground};
    }}

    [data-testid="stHeader"] {{
        background-color: {background};
    }}

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    label {{
        color: {foreground} !important;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background-color: {input_background};
        color: {foreground};
    }}

    input {{
        accent-color: #FF8C00 !important;
    }}

    div.stButton > button {{
        border-radius: 12px;
        min-height: 45px;
        font-weight: 600;
    }}
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 3. 세션 상태 초기화
# ==========================================

defaults = {
    "page": "list",
    "alarms": [],
    "active_alarm": None,
    "notice": "",
    "next_refresh": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 4. 수학 문제 생성
# ==========================================

def generate_problem(level):

    if level == "하":

        a = random.randint(10, 99)
        b = random.randint(1, 99)

        if random.choice([True, False]):
            return f"{a} + {b}", a + b

        return f"{a} - {b}", a - b

    elif level == "중":

        a = random.randint(2, 20)
        b = random.randint(2, 15)

        if random.choice([True, False]):
            return f"{a} × {b}", a * b

        return f"{a * b} ÷ {a}", b

    else:

        a = random.randint(5, 20)
        b = random.randint(5, 15)
        c = random.randint(1, a * b - 1)

        if random.choice([True, False]):
            return f"({a} × {b}) + {c}", a * b + c

        return f"({a} × {b}) - {c}", a * b - c


# ==========================================
# 5. 알람 소리 생성
# ==========================================

@st.cache_data
def make_alarm_sound():

    sample_rate = 44100
    duration = 0.6
    frequency = 880

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = []

        for i in range(int(sample_rate * duration)):

            value = int(
                12000 * math.sin(
                    2 * math.pi * frequency * i / sample_rate
                )
            )

            frames.append(struct.pack("<h", value))

        wav.writeframes(b"".join(frames))

    return buffer.getvalue()


# ==========================================
# 6. 시간 및 알람 확인
# ==========================================

now = datetime.datetime.now()

if st.session_state.active_alarm is None:

    due_alarms = [
        alarm for alarm in st.session_state.alarms
        if alarm["target"] <= now
    ]

    if due_alarms:

        alarm = min(
            due_alarms,
            key=lambda x: x["target"]
        )

        st.session_state.active_alarm = alarm["id"]

        if alarm["math"]:

            question, answer = generate_problem(
                alarm["difficulty"]
            )

            alarm["question"] = question
            alarm["answer"] = answer

        st.session_state.page = "ring"


# ==========================================
# 7. 알람 목록 화면
# ==========================================

def alarm_list_screen():

    apply_design(False)

    left, right = st.columns([5, 1])

    with left:
        st.markdown("# 알람")

    with right:
        if st.button("＋", use_container_width=True):
            st.session_state.page = "add"
            st.rerun()

    st.divider()

    if st.session_state.notice:

        st.success(st.session_state.notice)
        st.session_state.notice = ""

    if not st.session_state.alarms:

        st.markdown(
            "<h3 style='text-align:center; color:#999999;'>"
            "설정된 알람이 없습니다."
            "</h3>",
            unsafe_allow_html=True
        )

    else:

        for alarm in sorted(
            st.session_state.alarms,
            key=lambda x: x["target"]
        ):

            with st.container(border=True):

                st.markdown(
                    f"<h1 style='font-size:45px; margin:0;'>"
                    f"{alarm['period']} "
                    f"{alarm['hour']:02d}:{alarm['minute']:02d}"
                    f"</h1>",
                    unsafe_allow_html=True
                )

                if alarm["math"]:
                    st.caption(
                        f"수학 문제 사용 · 난이도 {alarm['difficulty']}"
                    )
                else:
                    st.caption("수학 문제 사용 안 함")


# ==========================================
# 8. 알람 추가 화면
# ==========================================

def alarm_add_screen():

    apply_design(True)

    st.markdown("# 알람 추가")
    st.divider()

    st.markdown("### 시간 설정")

    period = st.radio(
        "오전 / 오후",
        ["오전", "오후"],
        horizontal=True,
        key="period_select"
    )

    col1, col2 = st.columns(2)

    with col1:
        hour = st.selectbox(
            "시",
            list(range(1, 13)),
            index=6
        )

    with col2:
        minute = st.selectbox(
            "분",
            list(range(60)),
            format_func=lambda x: f"{x:02d}"
        )

    st.divider()

    st.markdown("### 수학 문제")

    math_enabled = st.toggle(
        "수학 문제 사용",
        value=True
    )

    difficulty = None

    if math_enabled:

        st.markdown("### 난이도 선택")

        difficulty = st.radio(
            "난이도",
            ["상", "중", "하"],
            horizontal=True,
            index=1,
            label_visibility="collapsed"
        )

    st.divider()

    if st.button(
        "저장",
        use_container_width=True,
        type="primary"
    ):

        hour_24 = hour % 12

        if period == "오후":
            hour_24 += 12

        current = datetime.datetime.now()

        target = datetime.datetime.combine(
            current.date(),
            datetime.time(hour_24, minute)
        )

        if target <= current:
            target += datetime.timedelta(days=1)

        new_alarm = {
            "id": str(uuid.uuid4()),
            "period": period,
            "hour": hour,
            "minute": minute,
            "math": math_enabled,
            "difficulty": difficulty,
            "target": target,
            "question": None,
            "answer": None
        }

        st.session_state.alarms.append(new_alarm)

        st.session_state.page = "list"
        st.rerun()

    if st.button("뒤로 가기", use_container_width=True):

        st.session_state.page = "list"
        st.rerun()


# ==========================================
# 9. 알람 실행 화면
# ==========================================

def alarm_ring_screen():

    apply_design(False)

    alarm_id = st.session_state.active_alarm

    alarm = next(
        (
            a for a in st.session_state.alarms
            if a["id"] == alarm_id
        ),
        None
    )

    if alarm is None:

        st.session_state.active_alarm = None
        st.session_state.page = "list"
        st.rerun()
        return

    st.markdown(
        f"""
        <h1 style="
            text-align:center;
            font-size:55px;
            margin-top:40px;
            color:#111111;
        ">
            {datetime.datetime.now().strftime("%H:%M:%S")}
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#777777;'>"
        "알람이 울리고 있습니다."
        "</p>",
        unsafe_allow_html=True
    )

    st.audio(
        make_alarm_sound(),
        format="audio/wav",
        autoplay=True,
        loop=True
    )

    st.divider()

    if alarm["math"]:

        st.markdown(
            "<h2 style='text-align:center;'>"
            "수학 문제를 풀어주세요"
            "</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h1 style="
                text-align:center;
                font-size:48px;
                margin:45px 0;
                color:#111111;
            ">
                {alarm['question']} = ?
            </h1>
            """,
            unsafe_allow_html=True
        )

        with st.form("answer_form"):

            answer = st.number_input(
                "답 입력",
                step=1,
                value=0
            )

            submitted = st.form_submit_button(
                "답 입력 완료",
                use_container_width=True
            )

            if submitted:

                if int(answer) == alarm["answer"]:

                    st.session_state.alarms = [
                        a for a in st.session_state.alarms
                        if a["id"] != alarm_id
                    ]

                    st.session_state.active_alarm = None
                    st.session_state.page = "list"
                    st.session_state.notice = "알람이 해제되었습니다!"

                    st.rerun()

                else:
                    st.error("오답입니다. 다시 입력하세요.")

    else:

        st.markdown(
            "<h2 style='text-align:center;'>"
            "알람을 끄려면 버튼을 눌러주세요."
            "</h2>",
            unsafe_allow_html=True
        )

        if st.button(
            "알람 끄기",
            use_container_width=True
        ):

            st.session_state.alarms = [
                a for a in st.session_state.alarms
                if a["id"] != alarm_id
            ]

            st.session_state.active_alarm = None
            st.session_state.page = "list"
            st.session_state.notice = "알람이 해제되었습니다!"

            st.rerun()


# ==========================================
# 10. 화면 실행 및 자동 갱신
# ==========================================

if st.session_state.active_alarm is not None:
    st.session_state.page = "ring"

if st.session_state.page == "list":
    alarm_list_screen()

elif st.session_state.page == "add":
    alarm_add_screen()

elif st.session_state.page == "ring":
    alarm_ring_screen()

# 알람이 설정되어 있으면 주기적으로 화면을 갱신
if st.session_state.alarms:

    time.sleep(1)
    st.rerun()
