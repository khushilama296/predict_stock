import streamlit as st
import numpy as np
import pandas as pd
import datetime as datetime

import plotly.graph_objects as go
import sklearn.preprocessing
import sklearn.linear_model
import sklearn.model_selection
from PIL import Image
import yfinance as yf
st.title("AIで株価予測アプリ")
st.write('AIを使って、株価を予測してみましょう。')

image = Image.open('stock_predict.png')
st.image(image, use_container_width=True)
st.write('あくまでAIによる予測です(参考値)。こちらのあぷりによる損害や損失は一切補償しかねます。')

st.header("株価銘柄のティッカーシンボルを入力してください。")
stock_name = st.text_input("例: AAPL, FB, SFTBY (大文字.小文字どちらでも可)", "AAPL")
stock_name = stock_name.upper()
link= 'https://yosshyjungle.sakura.ne.jp/oa_works/images/stock_predict.png'
st.markdown(link)
st.write('ティッカーシンボルについては上のリンク(SBI証券) をご参照ください。')

df_stock = yf.download(stock_name, '2021-01-05')
if isinstance(df_stock.columns, pd.MultiIndex):
    df_stock.columns = df_stock.columns.droplevel(1)
if df_stock.empty:
    st.error(f'エラー: {stock_name}のデータを取得できませんでした。ティッカーシンボルが正しいか確認してください。')
    st.stop()

st.header(stock_name + " 2022年1月5日から現在までの価格(USD)")
st.write(df_stock)

st.header(stock_name + " 終値と14日間平均(USD)")
df_stock['SMA'] = df_stock['Close'].rolling(window=14).mean()
df_stock2 = df_stock[['Close', 'SMA']]
st.line_chart(df_stock2)

st.header(stock_name + " 値動き(USD)")
df_stock['change'] = (((df_stock['Close'] - df_stock['Open'])) / (df_stock['Open']) * 100)
st.line_chart(df_stock['change'].tail(100))

fig = go.Figure(
    data=[go.Candlestick(
        x=df_stock.index,
        open=df_stock['Open'],
        high=df_stock['High'],
        low=df_stock['Low'],
        close=df_stock['Close'],
        increasing_line_color='green',
        decreasing_line_color='red',
    )
    ]
)

st.header(stock_name + " キャンドルスティング")
st.plotly_chart(fig, use_container_width=True)
