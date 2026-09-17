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
# 2. 장르 안에 영화가 들어 있는 트리맵
# =========================================================

st.header("2. 장르별 영화와 총 관객")

treemap_df = df.copy()

treemap_df["total_audi"] = pd.to_numeric(
    treemap_df["total_audi"],
    errors="coerce"
)

treemap_df["genre"] = (
    treemap_df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

treemap_df = treemap_df.dropna(
    subset=["genre", "movieNm", "total_audi"]
)

treemap_df = treemap_df[treemap_df["total_audi"] > 0]

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 안에 영화가 들어 있는 트리맵",
    labels={
        "genre": "장르",
        "movieNm": "영화",
        "total_audi": "총 관객"
    }
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="장르별로 어떤 영화가 많은 관객을 모았는지 한 문장으로 적어 보세요.",
    height=80,
    key="graph2_note"
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
# =========================================================
# 5. 장르별 총 관객 분포
# =========================================================

st.header("5. 장르별 총 관객 분포")

box_df = df.copy()

# 총 관객을 숫자로 변환
box_df["total_audi"] = pd.to_numeric(
    box_df["total_audi"],
    errors="coerce"
)

# 장르와 총 관객이 없는 행 제거
box_df = box_df.dropna(
    subset=["genre", "total_audi", "movieNm"]
)

# 영화가 10편 이상인 장르만 선택
genre_movie_counts = box_df["genre"].value_counts()

valid_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_df = box_df[
    box_df["genre"].isin(valid_genres)
]

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    points="outliers",
    color="genre",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객"
    },
    custom_data=["movieNm"]
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig5, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="장르별 총 관객의 분포와 차이를 한 문장으로 적어 보세요.",
    height=80,
    key="graph5_note"
)
# =========================================================
# 6. 첫 주 관객을 크기로 나타낸 버블 그래프
# =========================================================

st.header("6. 첫 주 관객과 총 관객의 관계")

bubble_df = df.copy()

# 숫자형으로 변환
bubble_df["first_scrn"] = pd.to_numeric(
    bubble_df["first_scrn"],
    errors="coerce"
)

bubble_df["total_audi"] = pd.to_numeric(
    bubble_df["total_audi"],
    errors="coerce"
)

bubble_df["first_week_audi"] = pd.to_numeric(
    bubble_df["first_week_audi"],
    errors="coerce"
)

# 필요한 값이 없는 행 제거
bubble_df = bubble_df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre"
    ]
)

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객 — 버블 크기는 첫 주 관객",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    },
    custom_data=["first_week_audi"]
)

fig6.update_traces(
    marker=dict(
        opacity=0.65,
        sizemin=5
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{customdata[0]:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig6, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="개봉일 스크린수, 첫 주 관객, 총 관객 사이의 관계를 한 문장으로 적어 보세요.",
    height=80,
    key="graph6_note"
)
# =========================================================
# 7. 제작 국가 → 장르 선버스트
# =========================================================

st.header("7. 제작 국가와 장르별 영화 구성")

sunburst_df = df.copy()

# 제작 국가와 장르가 없는 데이터 처리
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

# 국가 → 장르별 영화 편수 계산
sunburst_counts = (
    sunburst_df
    .groupby(["nation", "genre"])
    .size()
    .reset_index(name="영화 편수")
)

fig7 = px.sunburst(
    sunburst_counts,
    path=["nation", "genre"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 구성",
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "전체 비율: %{percentRoot:.1%}"
        "<extra></extra>"
    )
)

st.plotly_chart(fig7, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="제작 국가별로 어떤 장르의 영화가 많이 포함되어 있는지 한 문장으로 적어 보세요.",
    height=80,
    key="graph7_note"
)
# =========================================================
# 8. 10위권 체류 기간과 총 관객의 관계
# =========================================================

st.header("8. 10위권에 오래 머문 영화는 총 관객도 많은가")

scatter8_df = df.copy()

# 숫자형으로 변환
scatter8_df["days_in_top10"] = pd.to_numeric(
    scatter8_df["days_in_top10"],
    errors="coerce"
)

scatter8_df["total_audi"] = pd.to_numeric(
    scatter8_df["total_audi"],
    errors="coerce"
)

# 필요한 값이 없는 행 제거
scatter8_df = scatter8_df.dropna(
    subset=["days_in_top10", "total_audi", "movieNm"]
)

fig8 = px.scatter(
    scatter8_df,
    x="days_in_top10",
    y="total_audi",
    hover_name="movieNm",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "10위권에 머문 날수",
        "total_audi": "총 관객"
    }
)

fig8.update_traces(
    marker=dict(
        size=10,
        opacity=0.7
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "10위권에 머문 날수: %{x}일<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig8, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    placeholder="10위권에 머문 날수와 총 관객의 관계를 한 문장으로 적어 보세요.",
    height=80,
    key="graph8_note"
)
