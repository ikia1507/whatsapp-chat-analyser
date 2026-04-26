from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import os

extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(str(message).split())

    num_media_messages = df[df['message'].str.contains("Media omitted", na=False)].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(str(message)))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        temp = df[df['user'] == selected_user]
    else:
        temp = df

    temp = temp[~temp['message'].str.contains("Media omitted", na=False)]
    text = temp['message'].dropna().astype(str).str.cat(sep=" ")

    if text.strip() == "":
        return None

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(text)


def most_common_words(selected_user, df):

    file_path = os.path.join(os.path.dirname(__file__), "stop_hinglish.txt")
    stop_words = open(file_path, 'r', encoding='utf-8').read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains("Media omitted", na=False)]

    words = []

    for message in temp['message']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    common_words_list = Counter(words).most_common(20)

    return pd.DataFrame(common_words_list, columns=["word", "count"])


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in str(message) if emoji.is_emoji(c)])

    emoji_counter = Counter(emojis).most_common(20)

    return pd.DataFrame(emoji_counter, columns=["emoji", "count"])


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period',
                                  values='message', aggfunc='count').fillna(0)

    return user_heatmap
