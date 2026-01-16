import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import platform

# --- 폰트 설정 시작 ---
def set_korean_font():
    # 1. GitHub에 함께 올린 나눔고딕 파일 확인
    font_filename = "NanumGothic-Regular.ttf"
    
    if os.path.exists(font_filename):
        # 폰트 파일이 있는 경우 (Streamlit Cloud 환경 대응)
        font_prop = fm.FontProperties(fname=font_filename)
        plt.rc('font', family=font_prop.get_name())
        plt.rcParams['axes.unicode_minus'] = False
        return font_prop
    else:
        # 2. 로컬 환경인 경우 기존 방식 사용
        if platform.system() == 'Windows':
            plt.rc('font', family='Malgun Gothic')
        elif platform.system() == 'Darwin': # Mac
            plt.rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False
        return None

font_prop = set_korean_font()
# --- 폰트 설정 끝 ---

st.title("📊 국세청 근로소득 데이터 분석기 📊")
filepath = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try: 
    # 데이터 읽기 (인코딩 에러 방지를 위해 여러 설정 시도 권장)
    try:
        df = pd.read_csv(filepath, encoding='cp949')
    except:
        df = pd.read_csv(filepath, encoding='utf-8')
        
    st.success("✅ 데이터를 성공적으로 불러 왔습니다!")

    st.subheader("📊 데이터 확인하기")
    st.dataframe(df.head())

    st.subheader("📊 항목별 분포 그래프")

    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_columns:
        selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_columns)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col], ax=ax, color="#6DD66D", kde=True)

        # 폰트 속성 적용 (폰트 객체가 있을 경우를 대비)
        title_font = {'fontsize': 15, 'fontweight': 'bold'}
        if font_prop:
            ax.set_title(f"{selected_col} 분포 확인", fontproperties=font_prop, size=15, weight='bold')
            ax.set_xlabel(selected_col, fontproperties=font_prop, size=12)
            ax.set_ylabel("빈도수", fontproperties=font_prop, size=12)
        else:
            ax.set_title(f"{selected_col} 분포 확인", **title_font)
            ax.set_xlabel(selected_col)
            ax.set_ylabel("빈도수")

        st.pyplot(fig)
    else:
        st.warning("분석할 수 있는 숫자 데이터가 없습니다.")
    
except FileNotFoundError:
    st.error(f"❌ {filepath} 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")