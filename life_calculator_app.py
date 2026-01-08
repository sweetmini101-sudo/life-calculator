import streamlit as st
from datetime import date, timedelta
import pandas as pd
import math

st.set_page_config(page_title="인생 올인원 계산기", layout="centered")

st.title("🎉 인생 올인원 계산기")
st.caption("특별한 인생의 날 + 표준편차 석차 계산")

tab1, tab2 = st.tabs(["📅 인생의 특별한 날", "📊 표준편차 석차 계산기"])

# =========================
# 1️⃣ 인생 특별한 날 계산기
# =========================
with tab1:
    st.subheader("📅 인생의 특별한 날 계산기")
    st.markdown("""
**태어난 날을 기준으로**
- 전통 기념 나이 (환갑·칠순·팔순·백세)
- 숫자 기념일 (100일, 1,000일, 11,111일 등)
- 인생 이정표가 되는 날들을 모두 계산합니다.
""")

    birth = st.date_input("🎂 생년월일 선택", value=date(2000, 1, 1))
    today = date.today()

    special_days = [
        ("태어난 지 100일", 100, "아기 첫 기념일"),
        ("태어난 지 1,000일", 1000, "성장 이정표"),
        ("태어난 지 10,000일", 10000, "인생 큰 숫자 기념일"),
        ("태어난 지 11,111일", 11111, "숫자가 반복되는 상징적 날짜"),
        ("태어난 지 20,000일", 20000, "성인 이후 중요한 숫자 기념일"),
        ("태어난 지 30,000일", 30000, "인생 후반부 진입 상징"),
        ("환갑 (60세)", 60 * 365, "육십갑자 한 바퀴 완성"),
        ("칠순 (70세)", 70 * 365, "장수를 축하하는 나이"),
        ("팔순 (80세)", 80 * 365, "큰 장수의 상징"),
        ("구순 (90세)", 90 * 365, "아주 드문 장수"),
        ("백세 (100세)", 100 * 365, "인생 최고 경지")
    ]

    rows = []
    for name, days, desc in special_days:
        target_date = birth + timedelta(days=days)
        remain = (target_date - today).days
        weekday = target_date.strftime("%A")
        rows.append([
            name,
            desc,
            target_date,
            weekday,
            remain
        ])

    df = pd.DataFrame(
        rows,
        columns=["특별한 날", "의미 / 설명", "날짜", "요일", "남은 일수"]
    )

    st.dataframe(df, use_container_width=True)

    # 엑셀 저장
    file1 = "life_special_days.xlsx"
    df.to_excel(file1, index=False)

    with open(file1, "rb") as f:
        st.download_button(
            "📥 특별한 날 엑셀 다운로드",
            f,
            file_name=file1
        )

# =========================
# 2️⃣ 표준편차 석차 계산기
# =========================
with tab2:
    st.subheader("📊 표준편차 석차 계산기")
    st.markdown("""
**정규분포(Z점수)** 를 이용해  
전체 인원 중 **예상 석차**를 계산합니다.

- 표준편차 기본값: **15**
- 소수점 입력 가능
""")

    score = st.number_input("내 점수", value=100.0, step=0.1)
    mean = st.number_input("평균 점수", value=100.0, step=0.1)
    std = st.number_input("표준편차", value=15.0, step=0.1, min_value=0.1)
    total = st.number_input("전체 인원 수", value=100, min_value=1)

    z = (score - mean) / std
    percentile = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    rank = math.ceil((1 - percentile) * total)

    st.markdown("---")
    st.write(f"📌 **Z 점수:** {z:.3f}")
    st.write(f"📌 **상위 비율:** {percentile*100:.2f}%")
    st.write(f"🏆 **예상 석차:** {rank} / {total}")

    rank_df = pd.DataFrame([{
        "점수": score,
        "평균": mean,
        "표준편차": std,
        "전체 인원": total,
        "Z점수": round(z, 3),
        "상위비율(%)": round(percentile * 100, 2),
        "예상석차": rank
    }])

    file2 = "rank_result.xlsx"
    rank_df.to_excel(file2, index=False)

    with open(file2, "rb") as f:
        st.download_button(
            "📥 석차 결과 엑셀 다운로드",
            f,
            file_name=file2
        )
