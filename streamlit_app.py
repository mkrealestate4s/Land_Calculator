import streamlit as st
import math

st.set_page_config(page_title="공시지가 대비 매매호가 계산기", layout="centered")

st.title("🏗️ 공시지가 대비 매매호가 계산기")

# ===== 입력 =====
land_price = st.text_input("공시지가 (원 / ㎡)", placeholder="예: 5,000,000")
land_area = st.text_input("토지면적", placeholder="면적 입력")
unit = st.radio("면적 단위", ["㎡", "평"], horizontal=True)
sale_price_eok = st.text_input("현재 매매호가 (억원)", placeholder="예: 18")

# ===== 숫자 처리 함수 =====
def parse_number(value):
    try:
        return float(value.replace(",", ""))
    except:
        return None

def format_won(value):
    sign = "+" if value >= 0 else "-"
    value = abs(value)

    eok = int(value // 100_000_000)
    man = int((value % 100_000_000) // 10_000)

    result = ""
    if eok > 0:
        result += f"{eok}억 "
    if man > 0:
        result += f"{man:,}만원"

    return sign + result

# ===== 계산 =====
if st.button("계산하기"):
    land_price = parse_number(land_price)
    land_area = parse_number(land_area)
    sale_price_eok = parse_number(sale_price_eok)

    if not land_price or not land_area or not sale_price_eok:
        st.error("모든 값을 올바르게 입력해주세요.")
    else:
        # 토지가치 계산
        land_value = (
            land_price * land_area
            if unit == "㎡"
            else land_price * 3.3058 * land_area
        )

        sale_value = sale_price_eok * 100_000_000
        diff = sale_value - land_value
        ratio = (sale_value / land_value) * 100

        st.divider()

        st.subheader("📊 계산 결과")

        st.write(f"**공시지가 기준 토지가치:** {format_won(land_value)}")
        st.write(f"**현재 매매호가:** {sale_price_eok}억")

        if diff >= 0:
            st.markdown(f"**차이:** :red[{format_won(diff)}]")
        else:
            st.markdown(f"**차이:** :blue[{format_won(diff)}]")

        st.write(f"**공시지가 대비:** {ratio:.1f}%")

        # ===== 배터리형 시각화 =====
        st.subheader("🔋 공시지가 대비 프리미엄 체감도")

        max_blocks = 10
        filled_blocks = min(round((ratio / 200) * max_blocks), max_blocks)

        cols = st.columns(max_blocks)

        for i in range(max_blocks):
            if i < filled_blocks:
                if ratio <= 100:
                    color = "🟩"
                elif ratio <= 150:
                    color = "🟨"
                else:
                    color = "🟥"
            else:
                color = "⬜"

            cols[i].markdown(f"<div style='text-align:center;font-size:24px'>{color}</div>", unsafe_allow_html=True)

        if ratio > 200:
            st.warning("⚠ 공시지가 대비 과도한 프리미엄 구간입니다.")
