import streamlit as st 
import FinanceDataReader as fdr
import datetime

date=st.date_input("조회시작일을 선택:", datetime.datetime(2024,9,26))

code = st.text_input("종목코드", value="", placeholder="종목코드를 입력해주세요")

if code and date : 
    df=fdr.DataReader(code, date)
    data = df.sort_index(ascending=True).loc[:, 'Close']
    st.line_chart(data)
