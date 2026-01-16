import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 한글 폰트 설정 (환경에 따라 다름)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

st.title("📊 국세청 근로소득 데이터 분석기 📊")
filepath = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

# 폰트 경로 설정 (Streamlit Cloud 환경 대응)
@st.cache_resource
def load_font():
    # 이 부분은 리눅스 서버에 기본 설치된 폰트를 사용하거나 
    # 한글 지원을 위해 아래 설정을 추가합니다.
    plt.rc('font', family='NanumGothic') # 시스템에 나눔고딕이 있다면 사용
    plt.rcParams['axes.unicode_minus'] = False

try: 
    # 데이터 읽기
    df = pd.read_csv(filepath, encoding='cp949')
    st.success("✅ 데이터를 성공적으로 불러 왔습니다!")

    # 데이터 미리보기
    st.subheader("📊 데이터 확인하기")
    st.dataframe(df.head())

    # 데이터 분석 그래프 그리기
    st.subheader("📊 항목별 분포 그래프")

    # 숫자형 데이터가 있는 열만 선택하도록 필터링 (강사 추천 팁!)
    # 문자열 데이터로 히스토그램을 그리면 에러가 날 수 있습니다.
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_columns:
        selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_columns)

        # 그래프 그리기 (중복 제거 및 최적화)
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Seaborn 히스토그램
        sns.histplot(df[selected_col], ax=ax, color="#6DD66D", kde=True) # kde=True는 곡선을 그려줌

        # 그래프 제목 및 축 설정
        ax.set_title(f"{selected_col} 분포 확인", fontsize=15, fontweight='bold')
        ax.set_xlabel(selected_col, fontsize=12)
        ax.set_ylabel("빈도수", fontsize=12)

        # 스트림릿 웹 화면에 그래프 표시
        st.pyplot(fig)
    else:
        st.warning("분석할 수 있는 숫자 데이터가 없습니다.")
    
except FileNotFoundError:
    st.error(f"❌ {filepath} 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")