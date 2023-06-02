from urlextract import URLExtract
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()
from wordcloud import WordCloud


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for messages in df['message']:
        words.extend(messages.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == 'video omitted\n'].shape[0]

    # fetch number of Links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def fetch_most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['message'] != 'image omitted\n']
    temp = temp[temp['message'] != 'video omitted\n']
    temp = temp[temp['message'] != 'sticker omitted\n']
    temp = temp[temp['message'] != 'image omitted']
    temp = temp[temp['message'] != 'sticker omitted']
    temp = temp[temp['message'] != 'Contact card omitted']

    def remove_stop_words(message):
        y = []
        for word in message:
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['message'] != 'image omitted\n']
    temp = temp[temp['message'] != 'video omitted\n']
    temp = temp[temp['message'] != 'sticker omitted\n']
    temp = temp[temp['message'] != 'image omitted']
    temp = temp[temp['message'] != 'sticker omitted']
    temp = temp[temp['message'] != 'Contact card omitted']

    words = []

    for tem in temp['message']:
        for word in tem.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timelines = df.groupby('only_date').count()['message'].reset_index()

    return daily_timelines


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['date'].dt.day_name().value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns="period", values='message', aggfunc='count').fillna(0)

    return user_heatmap
