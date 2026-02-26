import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="나의 첫 AI 앱", page_icon="🎈")
st.title("🚀 나의 첫번째 AI 웹 서비스")

# 2. 사용자 입력 받기
name = st.text_input("당신의 이름은 무엇인가요?", "학생")
happiness = st.slider("오늘의 기분 점수는?", 0, 100, 50)

# 3. 버튼 클릭 이벤트
if st.button("축하 버튼 누르기"):
    st.balloons() # 화면에 풍선 애니메이션 효과
    st.success(f"반가워요, {name}님! 오늘의 기분 점수가 {happiness}점이군요!")

    # 간단한 가상 데이터 차트 보여주기
    st.subheader("📊 오늘의 에너지 분석")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['열정', '창의력', '집중력']
    )
    st.line_chart(chart_data)

# 4. 사이드바 꾸미기
st.sidebar.header("정보")
st.sidebar.info("이 앱은 스트림릿 클라우드를 통해 배포되었습니다.")