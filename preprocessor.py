import pandas as pd
import re 

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dates = [date.replace("\u202f", " ").strip(" - ") for date in dates]
    # Creating DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for msg in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', msg, maxsplit=1)  # Use maxsplit=1 to prevent extra splits
        if len(entry) > 2:  # If a username is found
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notif')
            messages.append(entry[0])

    # Assign lists to DataFrame
    df['users'] = users
    df['message'] = messages  
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df