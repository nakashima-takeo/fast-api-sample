"""Streamlitアプリケーション."""

import datetime
import json
import random

import requests
import streamlit as st

page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])

if page == "users":
    st.title("APIテスト画面（ユーザー）")

    with st.form(key="user"):
        user_id: int = random.randint(0, 10)
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"user_id": user_id, "user_name": user_name}
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("### 送信データ")
        st.json(data)
        st.write("### レスポンス結果")
        URL = "http://localhost:8000/users"
        res = requests.post(URL, json.dumps(data), timeout=10)
        st.write(res.status_code)
        st.write(res.json())

elif page == "rooms":
    st.title("APIテスト画面（会議室）")

    with st.form(key="room"):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = int(st.number_input("定員", step=1))
        data = {"room_id": room_id, "room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("### 送信データ")
        st.json(data)
        st.write("### レスポンス結果")
        URL = "http://localhost:8000/rooms"
        res = requests.post(URL, json.dumps(data), timeout=10)
        st.write(res.status_code)
        st.write(res.json())

elif page == "bookings":
    st.title("APIテスト画面（予約）")

    with st.form(key="booking"):
        booking_id: int = random.randint(0, 10)
        booking_user_id: int = random.randint(0, 10)
        booking_room_id: int = random.randint(0, 10)
        booked_num: int = int(st.number_input("予約人数", step=1))
        date = st.date_input("日付:", min_value=datetime.date.today())
        if not isinstance(date, datetime.date):
            date = datetime.date.today()
        start_time = st.time_input("開始時刻:", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻:", value=datetime.time(hour=20, minute=0))
        data = {
            "booking_id": booking_id,
            "user_id": booking_user_id,
            "room_id": booking_room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat(),
        }
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("### 送信データ")
        st.json(data)
        st.write("### レスポンス結果")
        URL = "http://localhost:8000/bookings"
        res = requests.post(URL, json.dumps(data), timeout=10)
        st.write(res.status_code)
        st.write(res.json())
