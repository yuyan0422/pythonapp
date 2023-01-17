import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import streamlit as st

st.title("株価チェックアプリ")

st.sidebar.write("""
# 株価
株価可視化ツールです。以下から表示日数を指定
""")

st.sidebar.write("""
## 表示日数
""")

days = st.sidebar.slider("日数", 1, 50, 20)

st.write(f"""
### **過去{days}日間**の株価
""")

# 3926.T
meigara = st.text_input("証券コードを入力してください")
ticker = f"{meigara}.T"

st.sidebar.write("""
    ## 株価の範囲指定
    """)
ymin, ymax = st.sidebar.slider(
"範囲指定",
0.0, 9000.0, (0.0, 9000.0)
)

#株価取得
df = yf.Ticker(ticker)
hist = df.history(period=f"{days}d")
# Dateの表示形式を変更する。
hist.index = hist.index.strftime("%d %B %Y")
# HISTの中のCloseのみを抽出
hist = hist[["Close"]]
# カラムの書き換え(会社名)
hist.columns=[ticker]
hist = hist.T
# 会社の上にNameをつける
hist.index.name = "Name"
data = hist.T.reset_index()
data.head()
# 元のテーブルの形に戻した（Meltで）
data = pd.melt(data, id_vars=["Date"]).rename(
    columns={"value": "Stock Prices(USD)"}
)
chart =(
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
        color="Name:N"
    )
)
st.altair_chart(chart, use_container_width=True)