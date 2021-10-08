import streamlit as st
import pandas as pd
import requests,datetime,json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

@st.cache
def get_covid_df(url):
    response_json = requests.get(url).json()
    df = pd.DataFrame(response_json['data'])
    return df
@st.cache
def get_vaccine_df(url2):
    response_json = requests.get(url2).json()
    df_v = pd.json_normalize(response_json, record_path='datasets')
    #df_v = pd.DataFrame(response_json['datasets'])
    return df_v

url = 'https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/daily_positive_detail.json'
url2 = 'https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/vaccination.json'
df_covid = get_covid_df(url)
df_vaccine = get_vaccine_df(url2)

diagnosed_date_list = df_covid['diagnosed_date'].values
str_maxdate = diagnosed_date_list[len(diagnosed_date_list)-1]
mindate = datetime.datetime.strptime(diagnosed_date_list[0], '%Y-%m-%d')
maxdate = datetime.datetime.strptime(str_maxdate, '%Y-%m-%d')
selected_date = st.sidebar.date_input(
    "感染者数表示期間",
    [mindate, maxdate],
    min_value=mindate,
    max_value=maxdate
)
str_startdate = selected_date[0].strftime('%Y-%m-%d')
str_enddate = selected_date[1].strftime(
    '%Y-%m-%d') if len(selected_date) == 2 else str_maxdate

"""
# 東京都COVID-19関連データ
### 感染者数 
"""

df_selected = df_covid.query(
    f'"{str_startdate}" <= diagnosed_date <= "{str_enddate}"')
st.write(df_selected)

# ワクチンデータフレーム表示
date_list = df_vaccine['date'].values
str_maxdate_v = date_list[len(date_list)-1]
mindate_v = datetime.datetime.strptime(date_list[0], '%Y-%m-%d')
maxdate_v = datetime.datetime.strptime(str_maxdate_v, '%Y-%m-%d')
selected_date_v = st.sidebar.date_input(
    "ワクチン接種者数表示期間",
    [mindate_v, maxdate_v],
    min_value=mindate_v,
    max_value=maxdate_v
)

str_startdate_v = selected_date_v[0].strftime('%Y-%m-%d')
str_enddate_v = selected_date_v[1].strftime(
    '%Y-%m-%d') if len(selected_date_v) == 2 else str_maxdate_v

"""
### ワクチン接種者数
"""

df_selected_v = df_vaccine.query(
    f'"{str_startdate_v}" <= date <= "{str_enddate_v}"')
st.write(df_selected_v)



"""
### 一日ごとの感染者数
"""

x = [
    datetime.datetime.strptime(diagnosed_date, '%Y-%m-%d')
    for diagnosed_date in df_selected['diagnosed_date'].values
]
y_count = df_selected['count'].values

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y_count)

wac_shown = st.sidebar.checkbox('一週間ごとの平均感染者数表示')
if wac_shown:
    y_weekly_average_count = df_selected['weekly_average_count'].values
    ax.plot(x, y_weekly_average_count)

xfmt = mdates.DateFormatter('%m/%d')
xloc = mdates.DayLocator(interval=20)

ax.xaxis.set_major_locator(xloc)
ax.xaxis.set_major_formatter(xfmt)
st.write(fig)

"""
### ワクチン接種者数
"""
x = [
    datetime.datetime.strptime(date, '%Y-%m-%d')
    for date in df_selected_v['date'].values
]
y_count = df_selected_v['data.cumulative_2nd_dose'].values

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y_count)

xfmt = mdates.DateFormatter('%m/%d')
xloc = mdates.DayLocator(interval=20)

ax.xaxis.set_major_locator(xloc)
ax.xaxis.set_major_formatter(xfmt)
st.write(fig)


"""
東京都新型コロナウイルス感染症対策サイトの[Github](https://github.com/tokyo-metropolitan-gov/covid19)より
"""