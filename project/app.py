import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="목포시민 카페 이용 실태 조사",
    page_icon="☕",
    layout="wide"
)

st.markdown("""
<style>

/* 사이드바 메뉴 글씨 크기 */
section[data-testid="stSidebar"] label {
    font-size: 20px !important;
    font-weight: bold;
}

/* 라디오 버튼 글씨 크기 */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    font-size: 18px !important;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# CSV 생성 및 불러오기
# ===============================

CSV_FILE = "responses.csv"

columns = [
    "거주지역",
    "연령",
    "성별",
    "이용빈도",
    "이용목적",
    "카페종류",
    "평균지출",
    "선택요소",
    "불편사항",
    "재방문의사",
    "응답시간"
]

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=columns)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

# ===============================
# 제목
# ===============================

st.title("☕ 목포시민 카페 이용 실태 및 만족도 조사")

st.markdown("---")

page = st.sidebar.radio(
    "메뉴",
    [
        "🏠 홈",
        "📝 설문 참여",
        "🔐 관리자"
    ]
)

# ===============================
# 홈
# ===============================

if page == "🏠 홈":

    st.header("앱 소개")

    st.write("""
본 설문은 **목포시민의 카페 이용 실태 및 만족도**를 조사하기 위한 앱입니다.

수집된 데이터는 통계 분석 목적으로만 활용됩니다.
""")

    st.subheader("조사 목적")

    st.markdown("""
- 카페 이용 빈도 조사
- 이용 목적 조사
- 카페 이용 패턴 분석
- 평균 소비 금액 분석
- 재방문 의사 조사
- 카페 선택 요소 조사
- 불편사항 조사
""")

    st.subheader("참여 대상")

    st.info("""
목포시에 거주하는 시민이라면 누구나 참여 가능합니다.
""")

    st.subheader("조사 절차")

    st.markdown("""
1. 설문 참여

2. 모든 문항 작성

3. 제출

4. 완료
""")

    st.success("왼쪽 메뉴에서 '설문 참여'를 선택해주세요.")

# ===============================
# 설문 페이지
# ===============================

elif page == "📝 설문 참여":

    st.header("설문조사")

    with st.form("survey"):

        area = st.selectbox(
            "1. 거주 지역",
            [
                "하당",
                "평화광장",
                "원도심",
                "옥암동",
                "용해동",
                "기타"
            ]
        )

        age = st.selectbox(
            "2. 연령",
            [
                "10대",
                "20대",
                "30대",
                "40대",
                "50대 이상"
            ]
        )

        gender = st.radio(
            "3. 성별",
            [
                "남성",
                "여성"
            ]
        )

        visit = st.radio(
            "4. 카페 이용 빈도",
            [
                "거의 가지 않음",
                "월 1~3회",
                "주 1~2회",
                "주 3회 이상"
            ]
        )

        purpose = st.radio(
            "5. 이용 목적",
            [
                "공부",
                "업무",
                "대화",
                "휴식",
                "기타"
            ]
        )

        cafe = st.radio(
            "6. 선호하는 카페 종류",
            [
                "프랜차이즈",
                "개인카페",
                "상관없음"
            ]
        )

        price = st.radio(
            "7. 평균 지출 금액",
            [
                "5천원 미만",
                "5천~1만원",
                "1만~2만원",
                "2만원 이상"
            ]
        )

        important = st.text_area(
            "8. 카페를 선택할 때 가장 중요하게 생각하는 요소를 작성해주세요."
        )

        inconvenience = st.text_area(
            "9. 카페 이용 시 가장 불편했던 점을 작성해주세요."
        )

        revisit = st.radio(
            "10. 다시 방문할 의향이 있습니까?",
            [
                "매우 그렇다",
                "그렇다",
                "보통",
                "아니다",
                "매우 아니다"
            ]
        )

        submit = st.form_submit_button("설문 제출")

    if submit:

        new_data = pd.DataFrame([{
            "거주지역": area,
            "연령": age,
            "성별": gender,
            "이용빈도": visit,
            "이용목적": purpose,
            "카페종류": cafe,
            "평균지출": price,
            "선택요소": important,
            "불편사항": inconvenience,
            "재방문의사": revisit,
            "응답시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        old = pd.read_csv(CSV_FILE)

        old = pd.concat(
            [old, new_data],
            ignore_index=True
        )

        old.to_csv(
            CSV_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("설문이 정상적으로 제출되었습니다.")

# ===============================
# 관리자 페이지
# ===============================
elif page == "🔐 관리자":

    st.header("🔐 관리자 페이지")

    password = st.text_input(
        "비밀번호를 입력하세요.",
        type="password"
    )

    if password == "1234":

        st.success("관리자 로그인 성공")

        df = pd.read_csv(CSV_FILE)

        st.markdown("---")

        tab1, tab2 = st.tabs(
            [
                "📊 실제 설문 결과",
                "🔍 실제 응답 vs 페르소나 비교"
            ]
        )


        # ==================================
        # 실제 설문 결과
        # ==================================
        with tab1:

            st.subheader("📊 응답 현황")

            st.metric(
                "총 응답자 수",
                len(df)
            )

            if len(df) == 0:
                st.warning("아직 응답 데이터가 없습니다.")
                st.stop()


            import plotly.express as px


            def draw_chart(column, title):

                count = (
                    df[column]
                    .value_counts()
                    .reset_index()
                )

                count.columns = [
                    column,
                    "응답수"
                ]


                fig = px.bar(
                    count,
                    x=column,
                    y="응답수",
                    text="응답수",
                    title=title
                )


                fig.update_layout(
                    showlegend=False
                )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            draw_chart("거주지역", "거주 지역")
            draw_chart("연령", "연령")
            draw_chart("성별", "성별")
            draw_chart("이용빈도", "카페 이용 빈도")
            draw_chart("이용목적", "카페 이용 목적")
            draw_chart("카페종류", "선호 카페 종류")
            draw_chart("평균지출", "평균 지출 금액")
            draw_chart("재방문의사", "재방문 의사")


            st.divider()


            st.subheader("📝 카페 선택 중요 요소")

            for i, text in enumerate(
                df["선택요소"],
                start=1
            ):

                if pd.notna(text) and str(text).strip():

                    st.write(
                        f"{i}. {text}"
                    )


            st.divider()


            st.subheader("📝 카페 이용 불편사항")

            for i, text in enumerate(
                df["불편사항"],
                start=1
            ):

                if pd.notna(text) and str(text).strip():

                    st.write(
                        f"{i}. {text}"
                    )


            st.divider()


            st.subheader("📄 전체 응답 데이터")

            st.dataframe(
                df,
                use_container_width=True
            )


            csv = df.to_csv(
                index=False,
                encoding="utf-8-sig"
            )


            st.download_button(
                "📥 CSV 다운로드",
                data=csv,
                file_name="responses.csv",
                mime="text/csv"
            )



        # ==================================
        # 실제 vs 페르소나 비교
        # ==================================
        with tab2:

            st.subheader(
                "🔍 실제 시민 응답과 페르소나 비교"
            )


            try:

                persona = pd.read_csv(
                    "persona_responses.csv"
                )


                st.write(
                    f"실제 응답 : {len(df)}명"
                )

                st.write(
                    f"페르소나 : {len(persona)}명"
                )


                def compare_chart(
                    column,
                    title
                ):


                    real = (
                        df[column]
                        .value_counts()
                        .reset_index()
                    )

                    real.columns = [
                        "항목",
                        "실제 응답"
                    ]


                    virtual = (
                        persona[column]
                        .value_counts()
                        .reset_index()
                    )

                    virtual.columns = [
                        "항목",
                        "페르소나"
                    ]


                    compare = pd.merge(
                        real,
                        virtual,
                        on="항목",
                        how="outer"
                    ).fillna(0)


                    compare = compare.melt(
                        id_vars="항목",
                        value_vars=[
                            "실제 응답",
                            "페르소나"
                        ],
                        var_name="구분",
                        value_name="인원"
                    )


                    fig = px.bar(
                        compare,
                        x="항목",
                        y="인원",
                        color="구분",
                        barmode="group",
                        title=title
                    )


                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


                compare_chart(
                    "이용목적",
                    "☕ 카페 이용 목적 비교"
                )


                compare_chart(
                    "카페종류",
                    "🏪 선호 카페 종류 비교"
                )


                compare_chart(
                    "이용빈도",
                    "⏰ 이용 빈도 비교"
                )


                compare_chart(
                    "평균지출",
                    "💰 평균 지출 비교"
                )


                compare_chart(
                    "재방문의사",
                    "🔁 재방문 의사 비교"
                )


            except FileNotFoundError:

                st.error(
                    "persona_responses.csv 파일을 찾을 수 없습니다."
                )


    elif password != "":

        st.error(
            "비밀번호가 올바르지 않습니다."
        )