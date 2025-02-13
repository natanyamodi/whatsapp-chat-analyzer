from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch total number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    # fetch number of media messages
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)


def fetch_most_busy_users(df):
    df = df[df['users'] != 'group_notif']
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename({'index':'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    temp = df[df['users']!= 'group_notif']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    temp = df[df['users']!= 'group_notif']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline