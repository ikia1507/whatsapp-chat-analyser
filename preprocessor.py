import re
import pandas as pd

def preprocess(data):

    pattern = r'(\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}[\u202f\s]?(?:AM|PM|am|pm))\s-\s'

    messages = re.split(pattern, data)[1:]
    
    dates = messages[0::2]      # even index
    msgs = messages[1::2]       # odd index

    df = pd.DataFrame({
        'user_message': msgs,
        'date': dates
    })

    df['date'] = df['date'].fillna("").astype(str).str.replace('\u202f', ' ', regex=False)

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p', errors='coerce')

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1].strip())
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # remove rows where date parsing failed
    df = df.dropna(subset=['date'])

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
