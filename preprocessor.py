import re
import pandas as pd

def preprocess(data):

    pattern = r'(\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2})\s-\s'

    parts = re.split(pattern, data)

    if len(parts) < 3:
        return pd.DataFrame()

    dates = parts[1::2]
    messages = parts[2::2]

    df = pd.DataFrame({"date": dates, "user_message": messages})

    df["date"] = df["date"].astype(str).str.replace("\u202f", " ", regex=False)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y, %H:%M", errors="coerce")

    users = []
    msgs = []

    for message in df["user_message"]:
        entry = re.split(r"([\w\W]+?):\s", message, maxsplit=1)

        if len(entry) > 2:
            users.append(entry[1].strip())
            msgs.append(entry[2])
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df["user"] = users
    df["message"] = msgs
    df.drop(columns=["user_message"], inplace=True)

    df = df.dropna(subset=["date"])

    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df["hour"]:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour+1}")

    df["period"] = period

    return df
