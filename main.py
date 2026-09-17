import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 8자리 숫자를 날짜로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 장르가 여러 개이면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    return df


df = load_data()


# =========================================================
# 1. 장르별 영화 편수
# =========================================================

st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.5,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    legend_title="장르"
)

st.plotly_chart(fig, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="장르별로 어떤 영화가 많이 개봉했는지 한 문장으로 적어 보세요.",
    height=80,
    key="graph1_note"
)
# =========================================================
# 3. 총 관객 분포
# =========================================================

st.header("3. 영화별 총 관객 분포")

# 총 관객을 숫자로 변환
df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce")

# 결측값 제거
hist_df = df.dropna(subset=["total_audi"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 관객이 많은 영화 찾기
max_movie = hist_df.loc[hist_df["total_audi"].idxmax()]

max_movie_name = max_movie["movieNm"]
max_movie_audi = int(max_movie["total_audi"])

# 가장 많이 몰린 구간 찾기
counts, bins = pd.cut(
    hist_df["total_audi"],
    bins=20,
    retbins=True
)
most_common_bin = counts.value_counts().idxmax()

st.info(
    f"대부분의 영화는 총 관객 **{most_common_bin.left:,.0f}명 ~ "
    f"{most_common_bin.right:,.0f}명** 구간에 몰려 있습니다. "
    f"가장 관객이 많은 영화는 **{max_movie_name}**으로, "
    f"총 **{max_movie_audi:,}명**입니다."
)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="영화들의 총 관객 수가 어느 구간에 많이 몰려 있는지 한 문장으로 적어 보세요.",
    height=80,
    key="graph3_note"
)
# =========================================================
# 4. 개봉일 스크린수와 총 관객의 관계
# =========================================================

st.header("4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df.copy()

# 숫자형으로 변환
scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"],
    errors="coerce"
)

scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"],
    errors="coerce"
)

# 필요한 값이 없는 행 제거
scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre"]
)

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(size=10, opacity=0.75),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig4, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="개봉일 스크린수와 총 관객 사이의 관계를 한 문장으로 적어 보세요.",
    height=80,
    key="graph4_note"
)
