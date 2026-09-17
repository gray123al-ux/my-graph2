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
