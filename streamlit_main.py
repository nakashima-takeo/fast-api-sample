"""Streamlitアプリケーション."""

import datetime
import json

import pandas as pd
import requests
import streamlit as st

page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])

if page == "users":
    st.title("ユーザー登録画面")

    with st.form(key="user"):
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {"name": user_name}
        submit_button = st.form_submit_button(label="ユーザー登録")

    if submit_button:
        URL = "http://localhost:8000/users"
        res = requests.post(URL, json.dumps(data), timeout=10)
        if res.status_code == 200:
            st.success("登録に成功しました")
        st.write(res.status_code)
        st.write(res.json())

elif page == "rooms":
    st.title("会議室登録画面")

    with st.form(key="room"):
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = int(st.number_input("定員", step=1))
        data = {"name": room_name, "capacity": str(capacity)}
        submit_button = st.form_submit_button(label="会議室作成")

    if submit_button:
        URL = "http://localhost:8000/rooms"
        res = requests.post(URL, json.dumps(data), timeout=10)
        if res.status_code == 200:
            st.success("登録に成功しました")
        st.write(res.status_code)
        st.write(res.json())

elif page == "bookings":
    st.title("会議室予約画面")

    # ユーザー情報取得
    URL = "http://localhost:8000/users"
    res = requests.get(URL, timeout=10)
    users = res.json()
    user_list = {user["name"]: user["id"] for user in users}
    inverse_user_list = {user["id"]: user["name"] for user in users}

    # 会議室情報取得
    URL = "http://localhost:8000/rooms"
    res = requests.get(URL, timeout=10)
    rooms = res.json()
    room_list = {room["name"]: room["id"] for room in rooms}
    inverse_room_list = {room["id"]: room["name"] for room in rooms}

    st.write("### 会議室情報")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = pd.Index(["会議室名", "定員", "会議室ID"])
    st.table(df_rooms)

    st.write("### 予約情報")
    URL = "http://localhost:8000/bookings"
    res = requests.get(URL, timeout=10)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)
    df_bookings["user_id"] = df_bookings["user_id"].map(inverse_user_list)
    df_bookings["room_id"] = df_bookings["room_id"].map(inverse_room_list)
    df_bookings["start_datetime"] = pd.to_datetime(
        df_bookings["start_datetime"]
    ).dt.strftime("%Y-%m-%d %H:%M")
    df_bookings["end_datetime"] = pd.to_datetime(
        df_bookings["end_datetime"]
    ).dt.strftime("%Y-%m-%d %H:%M")
    df_bookings.drop("id", axis=1, inplace=True)
    df_bookings.columns = pd.Index(
        ["ユーザー名", "会議室名", "予約人数", "開始時刻", "終了時刻"]
    )
    st.table(df_bookings)

    with st.form(key="booking"):
        booking_user_name = st.selectbox("ユーザー名", list(user_list.keys()))
        booking_room_name = st.selectbox("会議室名", list(room_list.keys()))
        booked_num: int = int(st.number_input("予約人数", step=1))
        date = st.date_input("日付:", min_value=datetime.date.today())
        if not isinstance(date, datetime.date):
            date = datetime.date.today()
        start_time = st.time_input("開始時刻:", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻:", value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        booking_user_id: int = user_list[booking_user_name]
        booking_room_id: int = room_list[booking_room_name]
        booking_room_capacity: int = [
            room["capacity"] for room in rooms if room["id"] == booking_room_id
        ][0]
        # 予約人数が定員を超えていないかチェック
        if booking_room_capacity < booked_num:
            st.error("予約人数が定員を超えています")
            st.stop()
        # 開始時刻が終了時刻より後になっていないかチェック
        if start_time >= end_time:
            st.error("開始時刻が終了時刻より後です")
            st.stop()
        # 予約が9:00-20:00の間になっているかチェック
        if (
            not datetime.time(hour=9, minute=0)
            <= start_time
            <= datetime.time(hour=20, minute=0)
        ):
            st.error("予約は9:00-20:00の間にしてください")
            st.stop()
        if (
            not datetime.time(hour=9, minute=0)
            <= end_time
            <= datetime.time(hour=20, minute=0)
        ):
            st.error("予約は9:00-20:00の間にしてください")
            st.stop()
        # 予約が重複していないかチェック
        for booking in bookings:
            if booking["room_id"] == booking_room_id:
                if datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=start_time.hour,
                    minute=start_time.minute,
                ) < datetime.datetime.fromisoformat(
                    booking["end_datetime"]
                ) and datetime.datetime(
                    year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=end_time.hour,
                    minute=end_time.minute,
                ) > datetime.datetime.fromisoformat(
                    booking["start_datetime"]
                ):
                    st.error("予約が重複しています")
                    st.stop()
        data = {
            "user_id": str(booking_user_id),
            "room_id": str(booking_room_id),
            "booked_num": str(booked_num),
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
        st.write("### 送信データ")
        st.json(data)
        st.write("### レスポンス結果")
        URL = "http://localhost:8000/bookings"
        res = requests.post(URL, json.dumps(data), timeout=10)
        if res.status_code == 200:
            st.success("登録に成功しました")
        else:
            st.error("登録に失敗しました")
        st.write(res.status_code)
