import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import streamlit as st
import requests


st.title("株価チェックアプリ")

st.sidebar.write("""
  ## 証券コードを記載後
   
  日数と範囲を選択してください
""")


# 3926.T
meigara = st.text_input("証券コードを入力してください")

ticker = f"{meigara}.T"

#証券コードが記載されたエクセルを読み込ませる
url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
r = requests.get(url)
with open('data_j.xls', 'wb') as output:
    output.write(r.content)
dd = pd.read_excel("./data_j.xls" , index_col="コード")



if meigara:
    # 証券コードの行から銘柄名を引っ張り出す
    value = dd.loc[int(meigara)]["銘柄名"]
    ##日数を選択してください
    st.sidebar.write("""
    ## 表示日数
    """)
    days = st.sidebar.slider("日数", 1, 60, 30)
    st.write(f"""
    ### {value}の株価({days}日間)
    """)
    
    ##範囲を選択してください
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
    "範囲指定",
    0.0, 4000.0, (500.0, 3000.0)
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