import streamlit as st
from datetime import datetime as dt 
import datetime


st.title("이것은 타이틀")
st.title('스마일 :sunglasses:')


st.header('헤더를 입력 :sparkles:')

st.subheader('이것은 subheader')

st.caption('캡션')

sample_code ='''
def function ():
    print('hellow world)
'''

st.code(sample_code, language='python')


st.metric(label="온도", value="10도", delta = '1.2도')
st.metric(label="삼성전자", value="61,000원", delta="-1,200원")


col1, col2, col3=st.columns(3)
col1.metric(label="온도", value="10도", delta = '1.2도')
col2.metric(label="온도", value="10도", delta = '1.2도')
col3.metric(label="온도", value="10도", delta = '1.2도')



st.text(dt.now())
st.text(dt.now().year)
st.text(dt.now().month)
st.text(dt.now().day)
st.text(dt.now().hour)
st.text(dt.now().minute)

if dt.now().minute % 2 ==1 :
    st.text("홀수")
else :
    st.text(dt.now().minute)


# 홀수일 경우 1 분 더한값으로 자르기 
start_time = st.slider("조회시작시간"
                       , min_value = dt(2024,1,1,0,0)
                       , max_value = dt(2024,1,7,23,1)
                       , value = dt(2024,1,3,12,0)
                       , step=datetime.timedelta(minutes=2)
                       , format = "YYYY-MM-DD - HH:mm")

end_time = st.slider("조회종료시간"
                       , min_value = dt(2024,1,1,0,0)
                       , max_value = dt(2024,1,7,23,0)
                       , value = dt(2024,1,3,12,0)
                       , step=datetime.timedelta(minutes=2)
                       , format = "YYYY-MM-DD - HH:mm")
st.write ("조회종료시간:", end_time)

number = st.number_input(label="나이를 입력"
                         , min_value=10
                         , max_value=100
                         , value=30
                         , step=5)

st.write(number)